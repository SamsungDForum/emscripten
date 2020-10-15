#include <array>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstring>
#include <iostream>
#include <mutex>
#include <poll.h>
#include <thread>
#include <sys/select.h>
#include <unistd.h>

namespace {
// Failed assert may cause select to block infinietly, so we print error
// message instead.
#define ASSERT(cond, text)      \
  if (!(cond)) {                \
    std::cout << text << "\n";  \
  }

using namespace std::chrono_literals;

constexpr const auto kSleepDuration = 1s;
constexpr const auto kAccurracy = 100ms;
constexpr const size_t kBufferSize = 32;
std::atomic_bool testPassed;
std::mutex cv_lock;
std::condition_variable cv;
bool shouldStartTest;

void errorMessage(const std::string& message) {
  // cout not cerr since we compare output file only with stdout.
  std::cout << message << ": " << strerror(errno) << "\n";
}

void sleepAndWrite(int fd_write) {
  {
    std::unique_lock<std::mutex> lock(cv_lock);
    cv.wait(lock, [] { return shouldStartTest; });
  }
  std::this_thread::sleep_for(kSleepDuration);

  std::array<char, kBufferSize> buffer;

  if (write(fd_write, buffer.data(), buffer.size()) == -1) {
    errorMessage("write failed");
  }
}

void testSelect(int fd_read, const struct timeval *tv, int expected) {
  fd_set rfds;
  FD_ZERO(&rfds);
  FD_SET(fd_read, &rfds);
  struct timeval* tv_ptr = NULL;
  struct timeval timeout;

  if (tv) {
    // copy timeout structure as select may change it.
    timeout.tv_sec = tv->tv_sec,
    timeout.tv_usec = tv->tv_usec,
    tv_ptr = &timeout;
  }

  {
    std::unique_lock<std::mutex> lock(cv_lock);
    cv.wait(lock, [] { return shouldStartTest; });
  }
  const auto time_before = std::chrono::steady_clock::now();
  const auto ret = select(fd_read + 1, &rfds, NULL, NULL, tv_ptr);
  const auto time_after = std::chrono::steady_clock::now();

  if (ret == -1) {
    errorMessage("select failed");
  } else if (ret == 0) {
    ASSERT(!FD_ISSET(fd_read, &rfds), "FD_ISSET");
  } else {
    ASSERT(ret == 1, "invalid select return value");
    ASSERT(FD_ISSET(fd_read, &rfds), "!FD_ISSET");
    const auto select_duration = time_after - time_before;
    ASSERT(kSleepDuration - kAccurracy < select_duration,
           "select took too long time");
    ASSERT(select_duration < kSleepDuration + kAccurracy,
           "select took too short time");

    std::array<char, kBufferSize> buffer;
    if (read(fd_read, buffer.data(), buffer.size()) == -1) {
      errorMessage("read failed");
    }
  }

  // Preserve failures.
  auto temp = true;
  testPassed.compare_exchange_strong(temp, ret == expected);
}

void testPoll(int fd_read, int timeout, int expected) {
  struct pollfd pollfd = {
    .fd = fd_read,
    .events = POLLIN,
    .revents = 0,
  };

  {
    std::unique_lock<std::mutex> lock(cv_lock);
    cv.wait(lock, [] { return shouldStartTest; });
  }

  const auto time_before = std::chrono::steady_clock::now();
  const auto ret = poll(&pollfd, 1, timeout);
  const auto time_after = std::chrono::steady_clock::now();

  if (ret == -1) {
    errorMessage("poll failed");
  } else if (ret == 0) {
   ASSERT(pollfd.revents == 0, "unexpected pollfd.revents value")
  } else {
    ASSERT(ret == 1, "invalid poll return value");
    ASSERT(pollfd.revents == POLLIN, "unexpected pollfd.revents value");
    const auto poll_duration = time_after - time_before;
    ASSERT(kSleepDuration - kAccurracy < poll_duration,
           "poll took too long time");
    ASSERT(poll_duration < kSleepDuration + kAccurracy,
           "poll took too short time");

    std::array<char, kBufferSize> buffer;
    if (read(fd_read, buffer.data(), buffer.size()) == -1) {
      errorMessage("read failed");
    }
  }

  // Preserve failures.
  auto temp = true;
  testPassed.compare_exchange_strong(temp, ret == expected);
}

void reportTestResults(const std::string& test) {
  if (testPassed) {
    std::cout << test << ": OK\n";
  } else {
    std::cout << test << ": FAIL\n";
  }
}

std::pair<int, int> makePipe() {
  int pipefd[2];
  if (pipe(pipefd) == -1) {
    errorMessage("pipe failed");
    exit(1);
  }
  int fd_read = pipefd[0];
  int fd_write = pipefd[1];
  return std::make_pair(fd_read, fd_write);
}

std::pair<int, int> prepareTest(bool shouldStart) {
  std::lock_guard<std::mutex> lock(cv_lock);
  shouldStartTest = shouldStart;
  testPassed = true;
  return makePipe();
}

void startTest() {
  std::lock_guard<std::mutex> lock(cv_lock);
  shouldStartTest = true;
  cv.notify_all();
}

void testSelectMain(const struct timeval *tv, int expected,
                    const std::string& test_description) {
  const auto [fd_read, fd_write] = prepareTest(true);
  std::thread t(sleepAndWrite, fd_write);
  testSelect(fd_read, tv, expected);

  t.join();
  reportTestResults("testSelectMain " + test_description);
}

void testPollMain(int timeout, int expected,
                  const std::string& test_description) {
  const auto [fd_read, fd_write] = prepareTest(true);
  std::thread t(sleepAndWrite, fd_write);
  testPoll(fd_read, timeout, expected);

  t.join();
  reportTestResults("testPollMain " + test_description);
}

void testSelectTwoThreads(const struct timeval *tv, int expected,
                          const std::string& test_description) {
  const auto [fd_read, fd_write] = prepareTest(false);
  std::thread t1(testSelect, fd_read, tv, expected);
  std::thread t2(sleepAndWrite, fd_write);

  startTest();

  t1.join();
  t2.join();
  reportTestResults("testSelectTwoThreads " + test_description);
}

void testPollTwoThreads(int timeout, int expected,
                        const std::string& test_description) {
  const auto [fd_read, fd_write] = prepareTest(false);
  std::thread t1(testPoll, fd_read, timeout, expected);
  std::thread t2(sleepAndWrite, fd_write);

  startTest();

  t1.join();
  t2.join();
  reportTestResults("testPollTwoThreads " + test_description);
}

int timevalToMsec(const struct timeval* tv) {
  if (!tv) {
    return -1;
  }
  return tv->tv_sec * 1'000 + tv->tv_usec / 1000;
}

void testManyCalls(const struct timeval *tv, int expected,
                   const std::string& test_description) {
  int timeout = timevalToMsec(tv);

  const auto [fd_read_0, fd_write_0] = prepareTest(false);
  std::thread t1(testPoll, fd_read_0, timeout, expected);
  std::thread t2(sleepAndWrite, fd_write_0);

  const auto [fd_read_1, fd_write_1] = makePipe();
  std::thread t3(testSelect, fd_read_1, tv, expected);
  std::thread t4(sleepAndWrite, fd_write_1);

  const auto [fd_read_2, fd_write_2] = makePipe();
  std::thread t5(testPoll, fd_read_2, timeout, expected);
  std::thread t6(sleepAndWrite, fd_write_2);

  startTest();

  t1.join();
  t2.join();
  t3.join();
  t4.join();
  t5.join();
  t6.join();
  reportTestResults("testManyCalls " + test_description);
}

void runTests(const struct timeval* tv, int expected,
              const std::string& description) {
  int timeout = timevalToMsec(tv);
  testSelectMain(tv, expected, description);
  testPollMain(timeout, expected, description);
  testSelectTwoThreads(tv, expected, description);
  testPollTwoThreads(timeout, expected, description);
  testManyCalls(tv, expected, description);
}
}  // namespace

int main() {
  struct timeval tv = { .tv_sec = 3, .tv_usec = 0 };
  int expected = 1;
  std::string description = "timeout 3s";
  runTests(&tv, expected, description);
  std::cout << "\n";

  tv = { .tv_sec = 0, .tv_usec = 0 };
  expected = 0;
  description = "timeout 0s";
  runTests(&tv, expected, description);
  std::cout << "\n";

  tv = { .tv_sec = 0, .tv_usec = 500 * 1000 };
  expected = 0;
  description = "timeout 500ms";
  runTests(&tv, expected, description);
  std::cout << "\n";

  expected = 1;
  description = "timeout NULL";
  runTests(NULL, expected, description);
}
