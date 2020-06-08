// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

const LibraryTizenEmss = {
  $CStructsOffsets: {
    ElementaryMediaStreamTrackConfig: {
      mimeType: 0,
      extradataSize: 4,
      extradata: 8,
    },
    ElementaryVideoStreamTrackConfig: {
      width: 12,
      height: 16,
      framerateNum: 20,
      framerateDen: 24,
    },
    ElementaryAudioStreamTrackConfig: {
      sampleFormat: 12,
      channelLayout: 16,
      samplesPerSecond: 20,
    },
    ElementaryMediaPacket: {
      pts: 0,
      dts: 8,
      duration: 16,
      isKeyFrame: 24,
      dataSize: 28,
      data: 32,
      width: 36,
      height: 40,
      framerateNum: 44,
      framerateDen: 48,
      sessionId: 52,
      subsamplesSize: 56,
      subsamples: 60,
      keyIdSize: 64,
      keyId: 68,
      initializationVectorSize: 72,
      initializationVector: 76,
      encryptionMode: 80,
    },
    MediaKeyConfig: {
      cdm: 0,
      encryptionMode: 4,
      licenseServer: 8,
      initDataSize: 12,
      initData: 16,
      audioMimeType: 20,
      audioRobustness: 24,
      videoMimeType: 28,
      videoRobustness: 32,
    },
  },

/*============================================================================*/
/*= Common code:                                                             =*/
/*============================================================================*/

  $EmssCommon__deps: ['$CStructsOffsets'],
  $EmssCommon__postset: 'EmssCommon.init();',
  $EmssCommon: {
    init: function() {
      // Matches samsung::wasm::kIgnoreSessionId
      const IGNORE_SESSION_ID = -1;

      // Matches samsung::wasm::OperationResult
      const Result = Object.freeze({
        SUCCESS: 0,
        WRONG_HANDLE: 1,
        INVALID_ARGUMENT: 2,
        INVALID_STATE: 3,
        LISTENER_ALREADY_SET: 4,
        NO_SUCH_LISTENER: 5,
        NOT_ALLOWED: 6,
        NOT_SUPPORTED: 7,
        ALREADY_DESTROYED: 8,
        ALREADY_IN_PROGRESS: 9,
        CLOSE_IN_PROGRESS: 10,
        NOT_ALLOWED_IN_CURRENT_MODE: 11,
        NO_TRACKS_ATTACHED: 12,
        OPEN_IN_PROGRESS: 13,
        PLAYBACK_STATE_CHANGE_IN_PROGRESS: 14,
        SOURCE_MUST_BE_CLOSED: 15,
        SOURCE_NOT_ATTACHED: 16,
        TIMESTAMPS_EXCEED_DURATION: 17,
        TRACK_LIMIT_REACHED: 18,
        UNRELATED_OBJECT: 19,
        FAILED: 20,

        // Config verification errors:
        INVALID_CHANNEL_LAYOUT: 21,
        INVALID_CODEC: 22,
        INVALID_FRAMERATE: 23,
        INVALID_RESOLUTION: 24,
        INVALID_MIME_TYPE: 25,
        INVALID_SAMPLE_FORMAT: 26,
        INVALID_CONFIG: 27,

        // Packet append errors:
        ABORTED: 28,
        BUFFER_FULL: 29,
        EXPECTS_KEYFRAME: 30,
        APPEND_IGNORED: 31,
        NO_DURATION: 32,
        INVALID_DTS: 33,
        INVALID_PTS: 34,
        INVALID_TRACK_STATE: 35,
        INVALID_VIDEO_PARAMETERS: 36,
        NO_PACKET_DATA: 37,
        RESOURCE_ALLOCATION: 38,

        // Encrypted packet append errors:
        DECRYPTION_ERROR: 39,
        DECRYPTOR_NEEDS_MORE_DATA: 40,
        NO_DECRYPTION_KEY: 41,
        INVALID_INITIALIZATION_VECTOR: 42,
        INVALID_KEY_ID: 43,
        INVALID_MEDIA_KEY_SESSION: 44,
        INVALID_SUBSAMPLE_DESCRIPTION: 45,
        UNKNOWN_DECRYPTION_MODE: 46,

        // Media key errors:
        INVALID_CONFIGRUATION: 47,
        SESSION_NOT_UPDATED: 48,

        // Video decoder errors:
        INVALID_TRACK_TYPE: 49,
        INVALID_VIDEO_TEXTURE: 50,
        WEBGL_CONTEXT_NOT_REGISTERED: 51,
        NOT_IN_VIDEO_TEXTURE_MODE: 52,
      });

      // C++ -> JS conversion maps (int-indexed arrays)

      const ERROR_TO_RESULT = new Map([
        // Elementary Media Stream Source errors:
        [ 'Adding new tracks is allowed only in \'closed\' state',            Result.SOURCE_MUST_BE_CLOSED         ],
        [ 'Cannot remove provided track: provided track was not created ' +
          'by this Elementary Media Stream Source instance.',                 Result.UNRELATED_OBJECT              ],
        [ 'Cannot set duration of a detached ElementaryMediaStreamSource.',   Result.SOURCE_NOT_ATTACHED           ],
        [ 'Duration cannot be set in Low Latency mode.',                      Result.NOT_ALLOWED_IN_CURRENT_MODE   ],
        [ 'ElementaryMediaStreamSource is not attached to HTMLMediaElement.', Result.SOURCE_NOT_ATTACHED           ],
        [ 'Exceeded maximum number of supported audio tracks (1)',            Result.TRACK_LIMIT_REACHED           ],
        [ 'Exceeded maximum number of supported video tracks (1)',            Result.TRACK_LIMIT_REACHED           ],
        [ 'Not attached to HTMLMediaElement.',                                Result.SOURCE_NOT_ATTACHED           ],
        [ 'Removing tracks is allowed only in \'closed\' state',              Result.SOURCE_MUST_BE_CLOSED         ],
        [ 'Setting duration below highest presentation timestamp of any buffered ' +
          'coded frames is disallowed. Instead, first call \'flush\'',        Result.TIMESTAMPS_EXCEED_DURATION    ],
        [ 'Cannot call while ElementaryMediaStreamSource.open() ' +
          'is in progress.',                                                  Result.OPEN_IN_PROGRESS              ],
        [ 'Cannot call while ElementaryMediaStreamSource.close() ' +
          'is in progress.',                                                  Result.CLOSE_IN_PROGRESS             ],
        [ 'Cannot invoke operation in the current readyState.',               Result.INVALID_STATE                 ],
        [ 'ElementaryMediaStreamSource is not attached to HTMLMediaElement.', Result.SOURCE_NOT_ATTACHED           ],
        [ 'Cannot open ElementaryMediaStreamSource with no tracks attached.', Result.NO_TRACKS_ATTACHED            ],
        // Variant of the above with misplaced dot due to bugged string in platform...
        [ 'Cannot open ElementaryMediaStreamSource.with no tracks attached.', Result.NO_TRACKS_ATTACHED            ],
        [ 'Player was already destroyed.',                                    Result.ALREADY_DESTROYED             ],
        [ 'Unknown error',                                                    Result.FAILED                        ],

        // Config verification errors:
        [ 'Invalid channel layout',                                           Result.INVALID_CHANNEL_LAYOUT        ],
        [ 'Invalid codec',                                                    Result.INVALID_CODEC                 ],
        [ 'Invalid framerate',                                                Result.INVALID_FRAMERATE             ],
        [ 'Invalid resolution',                                               Result.INVALID_RESOLUTION            ],
        [ 'No framerate in video config',                                     Result.INVALID_FRAMERATE             ],
        [ 'No mimetype in config',                                            Result.INVALID_MIME_TYPE             ],
        [ 'No resolution in video config',                                    Result.INVALID_RESOLUTION            ],
        [ 'Unknown audio codec',                                              Result.INVALID_CODEC                 ],
        [ 'Unknown sample format',                                            Result.INVALID_SAMPLE_FORMAT         ],
        [ 'Invalid video codec',                                              Result.INVALID_CODEC                 ],

        // Packet append errors:
        [ 'Append failed: aborted',                                           Result.ABORTED                       ],
        [ 'Append failed: cannot allocate internal resource',                 Result.RESOURCE_ALLOCATION           ],
        [ 'Append failed: buffer full',                                       Result.BUFFER_FULL                   ],
        [ 'Append failed: decryption error',                                  Result.DECRYPTION_ERROR              ],
        [ 'Append failed: more data needed',                                  Result.DECRYPTOR_NEEDS_MORE_DATA     ],
        [ 'Append failed: invalid track state',                               Result.INVALID_TRACK_STATE           ],
        [ 'Append failed: keyframe required',                                 Result.EXPECTS_KEYFRAME              ],
        [ 'Append failed: no decryption key',                                 Result.NO_DECRYPTION_KEY             ],
        [ 'Append failed: no media key session',                              Result.INVALID_MEDIA_KEY_SESSION     ],
        [ 'Append failed: unknown encryption',                                Result.UNKNOWN_DECRYPTION_MODE       ],
        [ 'Append failed: given set of video codec parameters (resolution ' +
          'and FPS) is unsupported',                                          Result.INVALID_VIDEO_PARAMETERS      ],
        [ 'Append failed: no framerate',                                      Result.INVALID_FRAMERATE             ],
        [ 'Append failed: no resolution',                                     Result.INVALID_RESOLUTION            ],
        [ 'Append failed: wrong session_id',                                  Result.APPEND_IGNORED                ],
        [ 'Append failed: unknown error',                                     Result.FAILED                        ],
        [ 'Append packet failed: missing pts',                                Result.INVALID_PTS                   ],
        [ 'Append packet failed: missing dts',                                Result.INVALID_DTS                   ],
        [ 'Append packet failed: negative pts',                               Result.INVALID_PTS                   ],
        [ 'Append packet failed: negative dts',                               Result.INVALID_DTS                   ],
        [ 'Append packet failed: missing duration',                           Result.NO_DURATION                   ],
        [ 'Append packet failed: if resolution is specified, both width ' +
          'and height must be provided',                                      Result.INVALID_RESOLUTION            ],
        [ 'Append packet failed: if framerate is specified, both ' +
          'framerateNum and framerateDen must be provided',                   Result.INVALID_FRAMERATE             ],
        [ 'Encrypted content in Video Texture mode is not supported.',        Result.NOT_ALLOWED_IN_CURRENT_MODE   ],
        [ 'Append packet failed: encrypted packet has no encrypted ' +
          'subsample description',                                            Result.INVALID_SUBSAMPLE_DESCRIPTION ],
        [ 'Append packet failed: each subsample must contain both '+
          'clearBytes and encryptedBytes fields',                             Result.INVALID_SUBSAMPLE_DESCRIPTION ],
        [ 'Append packet failed: missing keyId',                              Result.INVALID_KEY_ID                ],
        [ 'Append packet failed: bad keyId',                                  Result.INVALID_KEY_ID                ],
        [ 'Append packet failed: missing initializationVector',               Result.INVALID_INITIALIZATION_VECTOR ],
        [ 'Append packet failed: bad initializationVector',                   Result.INVALID_INITIALIZATION_VECTOR ],
        [ 'Append packet failed: missing encryptionMode',                     Result.UNKNOWN_DECRYPTION_MODE       ],
        [ 'Packet has no data.',                                              Result.NO_PACKET_DATA                ],
        [ 'Only one append is allowed at a time!',                            Result.ALREADY_IN_PROGRESS           ],
        [ 'Calling blocking append packet on main js thread is not allowed',  Result.NOT_ALLOWED                   ],

        // Video decoder errors:
        [ 'getPicture is already in progress',                                Result.ALREADY_IN_PROGRESS           ],
        [ 'This functionality is available only for video tracks.',           Result.INVALID_TRACK_TYPE            ],
        [ 'This functionality is available only for VideoTexture mode.',      Result.NOT_IN_VIDEO_TEXTURE_MODE     ],
        [ 'Invalid video texture provided.',                                  Result.INVALID_VIDEO_TEXTURE         ],
        [ 'Provided texture was not returned by getPicture method',           Result.INVALID_VIDEO_TEXTURE         ],
        [ 'Calling blocking get picture on main js thread is not allowed',    Result.NOT_ALLOWED                   ],
        [ 'WebGL rendering context not registered.',                          Result.WEBGL_CONTEXT_NOT_REGISTERED  ],

        // HTML Media Element errors:
        [ 'NotAllowedError',                                                  Result.NOT_ALLOWED                   ],
        [ 'NotSupportedError',                                                Result.NOT_SUPPORTED                 ],
        [ 'UnknownError',                                                     Result.FAILED                        ],
      ]);

      CHANNEL_LAYOUT_TO_STRING = [
        "ChannelLayoutNone",
        "ChannelLayoutUnsupported",
        "ChannelLayoutMono",
        "ChannelLayoutStereo",
        "ChannelLayout2Point1",
        "ChannelLayout2_1",
        "ChannelLayout2_2",
        "ChannelLayout3_1",
        "ChannelLayout4_0",
        "ChannelLayout4_1",
        "ChannelLayout4_1QuadSide",
        "ChannelLayout5_0",
        "ChannelLayout5_0Back",
        "ChannelLayout5_1",
        "ChannelLayout5_1Back",
        "ChannelLayout6_0",
        "ChannelLayout6_0Front",
        "ChannelLayout6_1",
        "ChannelLayout6_1Back",
        "ChannelLayout6_1Front",
        "ChannelLayout7_0",
        "ChannelLayout7_0Front",
        "ChannelLayout7_1",
        "ChannelLayout7_1Wide",
        "ChannelLayout7_1WideBack",
        "ChannelLayoutDiscrete",
        "ChannelLayoutHexagonal",
        "ChannelLayoutOctagonal",
        "ChannelLayoutQuad",
        "ChannelLayoutStereoDownmix",
        "ChannelLayoutSurround",
        "ChannelLayoutStereoAndKeyboardMic",
      ];

      const SAMPLE_FORMAT_TO_STRING = [
        "SampleFormatUnknown",
        "SampleFormatU8",
        "SampleFormatS16",
        "SampleFormatS32",
        "SampleFormatF32",
        "SampleFormatPlanarS16",
        "SampleFormatPlanarF32",
        "SampleFormatPlanarS32",
        "SampleFormatS24",
        "SampleFormatAc3",
        "SampleFormatEac3",
      ];

      EmssCommon = {
        Result: Result,
        _callFunction: function(handleMap, handle, name, ...args) {
          const obj = handleMap[handle];
          if (!obj) {
            console.error(`${name}(): invalid handle = '${handle}'`);
            return Result.WRONG_HANDLE;
          }

          obj[name](...args);

          return Result.SUCCESS;
        },
        _callAsyncFunction: function(
            handleMap, handle, getOperationResult,
            onFinishedCallback, userData, name, ...args) {
          const obj = handleMap[handle];
          if (!obj) {
            console.warn(`${name}(): invalid handle: '${handle}'`);
            return Result.WRONG_HANDLE;
          }
          obj[name](...args)
            .then(() => {
              {{{ makeDynCall('vii') }}} (
                onFinishedCallback, getOperationResult(null), userData);
            }).catch((err) => {
              {{{ makeDynCall('vii') }}} (
                onFinishedCallback, getOperationResult(err), userData);
            });
          return Result.SUCCESS;
        },
        _getProperty: function(handleMap, handle, property, retPtr, type) {
          const obj = handleMap[handle];
          if (!obj) {
            console.warn(`property ${property}: invalid handle = '${handle}'`);
            return Result.WRONG_HANDLE;
          }
          setValue(retPtr, obj[property], type);
          return Result.SUCCESS;
        },
        _setProperty: function(handleMap, handle, property, value) {
          const obj = handleMap[handle];
          if (!obj) {
            console.warn(`property ${property}: invalid handle = '${handle}'`);
            return Result.WRONG_HANDLE;
          }
          try {
            obj[property] = value;
          } catch (error) {
            console.error(error.message);
            return EmssCommon._exceptionToErrorCode(error);
          }
          return Result.SUCCESS;
        },
        _arrayFromPtr: function(object, ptrOffset, sizeOffset) {
          const ptr = {{{ makeGetValue('object', 'ptrOffset', 'i32') }}};
          const size = {{{ makeGetValue('object', 'sizeOffset', 'i32') }}};
          return new Uint8Array(HEAPU8.slice(ptr, ptr + size));
        },
        _extractBaseConfig: function(configPtr) {
          return {
            mimeType: UTF8ToString({{{ makeGetValue(
              'configPtr',
              'CStructsOffsets.ElementaryMediaStreamTrackConfig.mimeType',
              'i32') }}}),
            extradata: EmssCommon._arrayFromPtr(configPtr,
              CStructsOffsets.ElementaryMediaStreamTrackConfig.extradata,
              CStructsOffsets.ElementaryMediaStreamTrackConfig.extradataSize),
          };
        },
        _extendConfigTo: function(type, config, configPtr) {
          switch(type) {
            case 'audio':
              EmssCommon._extendConfigToAudio(config, configPtr);
              break;
            case 'video':
              EmssCommon._extendConfigToVideo(config, configPtr);
              break;
            default:
              console.error(`Invalid type: ${type}`);
          }
        },
        _cEnumToString: function(stringArray, value, defaultValueIndex = 0) {
          const ret = stringArray[value];
          if (ret == null) {
            return stringArray[defaultValueIndex];
          }
          return ret;
        },
        _exceptionToErrorCode: function(error) {
          if (error == null) {
            return Result.SUCCESS;
          }
          let errorMessage = error.message;
          const splitLine = errorMessage.search("': ");
          const errMsgLength = errorMessage.length;
          if(splitLine != -1) {
            errorMessage = errorMessage.slice(splitLine + 3, errMsgLength);
          }
          if (ERROR_TO_RESULT.has(errorMessage)) {
            return ERROR_TO_RESULT.get(errorMessage);
          }
          return Result.FAILED;
        },
        _sampleFormatToString: function(sampleFormat) {
          return EmssCommon._cEnumToString(
              SAMPLE_FORMAT_TO_STRING, sampleFormat);
        },
        _channelLayoutToString: function (channelLayout) {
          return EmssCommon._cEnumToString(
              CHANNEL_LAYOUT_TO_STRING, channelLayout);
        },
        _extendConfigToAudio: function(config, ptr) {
          config['sampleFormat'] = EmssCommon._sampleFormatToString(
            {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryAudioStreamTrackConfig.sampleFormat',
              'i32'); }}});
          config['channelLayout'] = EmssCommon._channelLayoutToString(
            {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryAudioStreamTrackConfig.channelLayout',
              'i32'); }}});
          config['samplesPerSecond'] = {{{ makeGetValue(
            'ptr',
            'CStructsOffsets.ElementaryAudioStreamTrackConfig.samplesPerSecond',
            'i32') }}};
        },
        _extendConfigToVideo: function(config, ptr) {
          config['width'] = {{{ makeGetValue(
            'ptr',
            'CStructsOffsets.ElementaryVideoStreamTrackConfig.width',
            'i32') }}};
          config['height'] = {{{ makeGetValue(
            'ptr',
            'CStructsOffsets.ElementaryVideoStreamTrackConfig.height',
            'i32') }}};
          config['framerateNum'] = {{{ makeGetValue(
            'ptr',
            'CStructsOffsets.ElementaryVideoStreamTrackConfig.framerateNum',
            'i32') }}};
          config['framerateDen'] = {{{ makeGetValue(
            'ptr',
            'CStructsOffsets.ElementaryVideoStreamTrackConfig.framerateDen',
            'i32') }}};
        },
        _makePacketFromPtr: function(ptr) {
          const config = {
            pts: {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.pts',
              'double') }}},
            dts: {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.dts',
              'double') }}},
            duration: {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.duration',
              'double') }}},
            isKeyFrame: {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.isKeyFrame',
              'i8') }}},
            isEncrypted: {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.isEncrypted',
              'i8') }}},
          };

          const sessionId = {{{ makeGetValue(
            'ptr',
            'CStructsOffsets.ElementaryMediaPacket.sessionId',
            'i32') }}};

          if (sessionId !== IGNORE_SESSION_ID) {
            config.sessionId = sessionId;
          }

          const framerateDen = {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.framerateDen',
              'i32') }}};

          const framerateNum = {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.framerateNum',
              'i32') }}};

          if (framerateDen !== 0 && framerateNum !== 0) {
            config.framerateDen = framerateDen;
            config.framerateNum = framerateNum;
          }

          const height = {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.height',
              'i32') }}};

          const width = {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.width',
              'i32') }}};

          if (height !== 0 && width !== 0) {
            config.height = height;
            config.width = width;
          }

          config.isEncrypted = false;
          return config;
        },
        _extendPacketToEncrypted: function(packet, ptr) {
          const pad = (array, goalLength = 16) => {
            const padding = new Array(goalLength - array.length).fill(0);
            return new Uint8Array([
              ...array,
              ...padding]);
          };

          packet.isEncrypted = true;
          packet.keyId = pad(EmssCommon._arrayFromPtr(ptr,
            CStructsOffsets.ElementaryMediaPacket.keyId,
            CStructsOffsets.ElementaryMediaPacket.keyIdSize));
          packet.initializationVector = pad(EmssCommon._arrayFromPtr(ptr,
            CStructsOffsets.ElementaryMediaPacket.initializationVector,
            CStructsOffsets.ElementaryMediaPacket.initializationVectorSize));
          packet.encryptionMode = EmssMediaKey._encryptionModeToString(
            {{{ makeGetValue(
              'ptr',
              'CStructsOffsets.ElementaryMediaPacket.encryptionMode',
              'i32') }}});
          packet.subsamples = EmssMediaKey._getSubsamples(ptr);
        },
        _makePacketDataFromPtr: function(ptr) {
          const dataPtr = {{{ makeGetValue(
            'ptr',
            'CStructsOffsets.ElementaryMediaPacket.data',
            'i32') }}};
          const dataSize = {{{ makeGetValue(
            'ptr',
            'CStructsOffsets.ElementaryMediaPacket.dataSize',
            'i32') }}};
          return new Uint8Array(HEAPU8.buffer, dataPtr, dataSize);
        },
        _setListener: function(namespace, handle, eventName, eventHandler) {
          const obj = namespace.handleMap[handle];
          if (!obj) {
            console.warn(
                `Set listener ${eventName}: invalid handle = '${handle}'`);
            return Result.WRONG_HANDLE;
          }
          if (eventName in namespace.listenerMap[handle]) {
            console.warn(`Listener already set: '${eventName}'`);
            return Result.LISTENER_ALREADY_SET;
          }
          namespace.listenerMap[handle][eventName] = eventHandler;
          obj.addEventListener(eventName, eventHandler);
          return Result.SUCCESS;
        },
        _unsetListener: function(namespace, handle, eventName) {
          const obj = namespace.handleMap[handle];
          if (!obj) {
            console.warn(
              `Unset listener ${eventName}: invalid handle = '${handle}'`);
            return Result.WRONG_HANDLE;
          }
          if (!(eventName in namespace.listenerMap[handle])) {
            return Result.NO_SUCH_LISTENER;
          }
          obj.removeEventListener(
              eventName,
              namespace.listenerMap[handle][eventName]);
          delete namespace.listenerMap[handle][eventName];
          return Result.SUCCESS;
        },
        _clearListeners: function(namespace, handle) {
          const obj = namespace.handleMap[handle];
          if (!obj) {
            console.warn(`clear listeners: invalid handle = '${handle}'`);
            return Result.WRONG_HANDLE;
          }
          const listeners = namespace.listenerMap[handle];
          Object.entries(listeners).forEach((eventArr) => {
              obj.removeEventListener(eventArr[0], eventArr[1]);
          });
          namespace.listenerMap[handle] = {};
          return Result.SUCCESS;
        },
      };
    },
  },

/*============================================================================*/
/*= samsung::wasm::MediaKey impl:                                            =*/
/*============================================================================*/

  $EmssMediaKey__deps: ['$EmssCommon'],
  $EmssMediaKey: {
    handleMap: [],
    _cdmToString: function(cdm) {
      return EmssCommon._cEnumToString([
          'unknown',
          'playready',
          'widevine',
        ], cdm);
    },
    _encryptionModeToString: function(encryptionMode) {
      return EmssCommon._cEnumToString([
          'unknown',
          'cenc',
          'cbcs'
        ], encryptionMode);
    },
    _robustnessToString: function(robustness) {
      return EmssCommon._cEnumToString([
          '',
          'SW_SECURE_CRYPTO',
          'SW_SECURE_DECODE',
          'HW_SECURE_CRYPTO',
          'HW_SECURE_DECODE',
          'HW_SECURE_ALL',
        ], robustness);
    },
    _makeDRMConfigFromPtr: function(drmConfigPtr) {
      const config = {
        cdm: EmssMediaKey._cdmToString(
          {{{ makeGetValue(
            'drmConfigPtr',
            'CStructsOffsets.MediaKeyConfig.cdm',
            'i32') }}}),
        encryptionMode: EmssMediaKey._encryptionModeToString(
          {{{ makeGetValue(
            'drmConfigPtr',
            'CStructsOffsets.MediaKeyConfig.encryptionMode',
            'i32') }}}),
        licenseServer: UTF8ToString({{{ makeGetValue(
          'drmConfigPtr',
          'CStructsOffsets.MediaKeyConfig.licenseServer',
          'i32') }}}),
        audioMimeType: UTF8ToString({{{ makeGetValue(
          'drmConfigPtr',
          'CStructsOffsets.MediaKeyConfig.audioMimeType',
          'i32') }}}),
        audioRobustness: EmssMediaKey._robustnessToString(
          {{{ makeGetValue(
            'drmConfigPtr',
            'CStructsOffsets.MediaKeyConfig.audioRobustness',
            'i32') }}}),
        videoMimeType: UTF8ToString({{{ makeGetValue(
          'drmConfigPtr',
          'CStructsOffsets.MediaKeyConfig.videoMimeType',
          'i32') }}}),
        videoRobustness: EmssMediaKey._robustnessToString(
          {{{ makeGetValue(
            'drmConfigPtr',
            'CStructsOffsets.MediaKeyConfig.videoRobustness',
            'i32') }}}),
        initData: EmssCommon._arrayFromPtr(drmConfigPtr,
          CStructsOffsets.MediaKeyConfig.initData,
          CStructsOffsets.MediaKeyConfig.initDataSize),
      };
      return config;
    },
    _getSubsamples: function(packetPtr) {
      const arrayToInt32 = (arraySlice) => {
        return arraySlice.map((value, index) => {
          return value << (index * 8);
        }).reduce((acc, val) => {
          return acc + val;
        }, 0);
      };
      const chunk = (array, begin, size) => {
        return array.slice(begin, begin + size);
      };
      const subsampleSize = 8;
      const ptr = {{{ makeGetValue(
        'packetPtr',
        'CStructsOffsets.ElementaryMediaPacket.subsamples',
        'i32') }}};
      const size = {{{ makeGetValue(
        'packetPtr',
        'CStructsOffsets.ElementaryMediaPacket.subsamplesSize',
        'i32') }}};
      const subsamples = Array.from(HEAPU8.slice(
        ptr, ptr + size * subsampleSize));
      const ret = [];
      for (let subsample = 0;
          subsample < size * subsampleSize;
          subsample += subsampleSize) {
        ret.push({
          clearBytes: arrayToInt32(chunk(subsamples, subsample, 4)),
          encryptedBytes: arrayToInt32(chunk(subsamples, subsample + 4, 4)),
        });
      }
      return ret;
    },
    _initSession: function(config, mediaKeys) {
      const session = mediaKeys.createSession();
      const licenseUpdated = new Promise((resolve, reject) => {
        session.onmessage = (event) => {
          this._onSessionMessage(
            event, config.licenseServer, resolve, reject);
        };
      });

      return session.generateRequest(config.encryptionMode, config.initData)
        .then(() => { return licenseUpdated; })
        .then(() => { return [mediaKeys, session]; },
              () => { throw  new Error("SessionNotUpdatedError"); });
    },
    _setupMediaKey: function(config) {
      return this._getMediaKeys(config)
        .then((mediaKeys) => { return this._initSession(config, mediaKeys); },
              () => { throw new Error("InvalidConfigurationError"); });
    },
    _getMediaKeys: function(config) {
      const keySystem = {
        playready: 'com.microsoft.playready',
        widevine: 'com.widevine.alpha',
      }[config.cdm];

      return navigator.requestMediaKeySystemAccess(
          keySystem,
          [this._prepareSupportedConfiguration(config)])
        .then(mediaKeySystemAccess => {
            return mediaKeySystemAccess.createMediaKeys();
        });
    },
    _prepareSupportedConfiguration: function(config) {
      const supportedConfigurations = {
        initDataTypes: [config.encryptionMode],
      };
      const configs = [
        ['audio', config.audioMimeType, config.audioRobustness],
        ['video', config.videoMimeType, config.videoRobustness]
      ];
      // Don't use destructuring assignment, as it breaks linking with -Os
      for (const cfg of configs) {
        const trackType = cfg[0];
        const mimeType = cfg[1];
        const robustness = cfg[2];
        if (mimeType) {
          supportedConfigurations[`${trackType}Capabilities`] = [{
            contentType: mimeType,
            robustness: robustness,
          }];
        }
      }
      return supportedConfigurations;
    },
    _onSessionMessage: function(event, licenseServer, resolve, reject) {
      const xmlhttp = new XMLHttpRequest();
      xmlhttp.open('POST', licenseServer);
      xmlhttp.responseType = 'arraybuffer';
      xmlhttp.setRequestHeader('Content-Type', 'text/xml; charset=utf-8');
      xmlhttp.onreadystatechange = () => {
        this._onReadyStateChange(
          xmlhttp, event, resolve, reject);
      };
      xmlhttp.send(event.message);
    },
    _onReadyStateChange: function(xmlhttp, event, resolve, reject) {
      if (xmlhttp.readyState != 4) {
        return Promise.resolve().then(() => undefined);
      }

      const responseString = String.fromCharCode(
          ...new Uint8Array(xmlhttp.response)).split('\r\n').pop();
      const license = new Uint8Array(
          Array.from(responseString).map((c) => c.charCodeAt(0)));
      return event.target.update(license)
        .then(() => { resolve(); },
              (error) => {
            console.error(`Failed to update the session: ${error}`);
            reject(error);
        });
    },
  },

/*============================================================================*/
/*= samsung::wasm::MediaKey bindings:                                        =*/
/*============================================================================*/

  mediaKeySetEncryption__deps: ['$EmssCommon', '$EmssMediaKey'],
  mediaKeySetEncryption__proxy: 'sync',
  mediaKeySetEncryption: function(configPtr, onFinished, userData) {
    let config = {};
    try {
      config = EmssMediaKey._makeDRMConfigFromPtr(configPtr);
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
    EmssMediaKey._setupMediaKey(config).then(
      ([mediaKeys, mediaKeySession]) => {
        const id = EmssMediaKey.handleMap.length;
        EmssMediaKey.handleMap[id] = {
          mediaKeys,
          mediaKeySession,
        };
        {{{ makeDynCall('viii') }}} (
          onFinished,
          EmssCommon.Result.SUCCESS,
          id,
          userData);
      }).catch((error) => {
        console.error(error.message);
        const errorCode = EmssCommon._exceptionToErrorCode(error);
        {{{ makeDynCall('viii') }}} (onFinished, errorCode, -1, userData);
      });
    return EmssCommon.Result.SUCCESS;
  },

  mediaKeyRemove__deps: ['$EmssCommon', '$EmssMediaKey'],
  mediaKeyRemove__proxy: 'sync',
  mediaKeyRemove: function(handle) {
    const obj = EmssMediaKey.handleMap[handle];
    if (!obj) {
      console.error(`remove media key: invalid handle = '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }

    try {
      obj.mediaKeySession.close().catch((exception) => {
        console.error(`failed to close media key session:` +
                      `'${exception.message}'`);
      });
    } catch (exception) {
      console.error(`failed to close media key session:` +
                    `'${exception.message}'`);
      return EmssCommon.Result.FAILED;
    }

    return EmssCommon.Result.SUCCESS;
  },

/*============================================================================*/
/*= samsung::html::HTMLMediaElement impl:                                    =*/
/*============================================================================*/

  $WasmHTMLMediaElement__deps: ['$EmssCommon'],
  $WasmHTMLMediaElement__postset: 'WasmHTMLMediaElement.init();',
  $WasmHTMLMediaElement: {
    init: function() {
      WasmHTMLMediaElement = {
        handleMap: [],
        listenerMap: {},
        _callFunction: function(handle, name, ...args) {
          return EmssCommon._callFunction(
            WasmHTMLMediaElement.handleMap,
            handle,
            name,
            ...args);
        },
        _callAsyncFunction: function(
            handle, onFinished, userData, name, ...args) {
          return EmssCommon._callAsyncFunction(
            WasmHTMLMediaElement.handleMap,
            handle,
            EmssCommon._exceptionToErrorCode,
            onFinished,
            userData,
            name,
            ...args);
        },
        _getProperty: function(handle, property, retPtr, type) {
          return EmssCommon._getProperty(
            WasmHTMLMediaElement.handleMap, handle, property, retPtr, type);
        },
        _setProperty: function(handle, property, value) {
          return EmssCommon._setProperty(
            WasmHTMLMediaElement.handleMap, handle, property, value);
        },
        _setListener: function(handle, eventName, eventHandler) {
          return EmssCommon._setListener(
            WasmHTMLMediaElement, handle, eventName, eventHandler);
        },
        _unsetListener: function(handle, eventName) {
          return EmssCommon._unsetListener(
            WasmHTMLMediaElement, handle, eventName);
        },
      };
    },
  },

/*============================================================================*/
/*= samsung::html::HTMLMediaElement bindings:                                =*/
/*============================================================================*/

  mediaElementById__deps: ['$WasmHTMLMediaElement'],
  mediaElementById__proxy: 'sync',
  mediaElementById: function(id) {
    const strId = UTF8ToString(id);
    const mediaElement = document.getElementById(strId);
    if (!mediaElement) {
      console.error(`No such media element: '${strId}'`);
      return -1;
    }
    const handle = WasmHTMLMediaElement.handleMap.length;
    WasmHTMLMediaElement.handleMap[handle] = mediaElement;
    WasmHTMLMediaElement.listenerMap[handle] = {};
    return handle;
  },

  mediaElementRemove__deps: ['$EmssCommon', '$WasmHTMLMediaElement'],
  mediaElementRemove__proxy: 'sync',
  mediaElementRemove: function(handle) {
    if (!(handle in WasmHTMLMediaElement.handleMap)) {
      console.error(`No such media element: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }
    WasmHTMLMediaElement.handleMap[handle].src = '';
    EmssCommon._clearListeners(WasmHTMLMediaElement, handle);
    delete WasmHTMLMediaElement.handleMap[handle];
    delete WasmHTMLMediaElement.listenerMap[handle];
    return EmssCommon.Result.SUCCESS;
  },

  mediaElementIsAutoplay__deps: ['$WasmHTMLMediaElement'],
  mediaElementIsAutoplay__proxy: 'sync',
  mediaElementIsAutoplay: function(handle, retPtr) {
    return WasmHTMLMediaElement._getProperty(
      handle, 'autoplay', retPtr, 'i8');
  },

  mediaElementSetAutoplay__deps: ['$WasmHTMLMediaElement'],
  mediaElementSetAutoplay__proxy: 'sync',
  mediaElementSetAutoplay: function(handle, newAutoplay) {
    return WasmHTMLMediaElement._setProperty(
      handle, 'autoplay', newAutoplay);
  },

  mediaElementGetCurrentTime__deps: ['$WasmHTMLMediaElement'],
  mediaElementGetCurrentTime__proxy: 'sync',
  mediaElementGetCurrentTime: function(handle, retPtr) {
    return WasmHTMLMediaElement._getProperty(
      handle, 'currentTime', retPtr, 'double');
  },

  mediaElementSetCurrentTime__deps: ['$WasmHTMLMediaElement'],
  mediaElementSetCurrentTime__proxy: 'sync',
  mediaElementSetCurrentTime: function(handle, newCurrentTime) {
    return WasmHTMLMediaElement._setProperty(
      handle, 'currentTime', newCurrentTime);
  },

  mediaElementGetDuration__deps: ['$WasmHTMLMediaElement'],
  mediaElementGetDuration__proxy: 'sync',
  mediaElementGetDuration: function(handle, retPtr) {
    return WasmHTMLMediaElement._getProperty(
      handle, 'duration', retPtr, 'double');
  },

  mediaElementIsEnded__deps: ['$WasmHTMLMediaElement'],
  mediaElementIsEnded__proxy: 'sync',
  mediaElementIsEnded: function(handle, retPtr) {
    return WasmHTMLMediaElement._getProperty(
      handle, 'ended', retPtr, 'i8');
  },

  mediaElementIsLoop__deps: ['$WasmHTMLMediaElement'],
  mediaElementIsLoop__proxy: 'sync',
  mediaElementIsLoop: function(handle, retPtr) {
    return WasmHTMLMediaElement._getProperty(
      handle, 'loop', retPtr, 'i8');
  },

  mediaElementSetLoop__deps: ['$WasmHTMLMediaElement'],
  mediaElementSetLoop__proxy: 'sync',
  mediaElementSetLoop: function(handle, newLoop) {
    return WasmHTMLMediaElement._setProperty(
      handle, 'loop', newLoop);
  },

  mediaElementIsPaused__deps: ['$WasmHTMLMediaElement'],
  mediaElementIsPaused__proxy: 'sync',
  mediaElementIsPaused: function(handle, retPtr) {
    return WasmHTMLMediaElement._getProperty(
      handle, 'paused', retPtr, 'i8');
  },

  mediaElementGetReadyState__deps: ['$WasmHTMLMediaElement'],
  mediaElementGetReadyState__proxy: 'sync',
  mediaElementGetReadyState: function(handle, retPtr) {
    return WasmHTMLMediaElement._getProperty(
      handle, 'readyState', retPtr, 'i32');
  },

  mediaElementGetSrc__deps: ['$EmssCommon', '$WasmHTMLMediaElement'],
  mediaElementGetSrc__proxy: 'sync',
  mediaElementGetSrc: function(handle, retPtr) {
    const mediaElement = WasmHTMLMediaElement.handleMap[handle];
    if (!mediaElement) {
      console.warn(`No such media element: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }

    const src = mediaElement.src.toString();
    const length = lengthBytesUTF8(src) + 1;
    const ptr = _malloc(length);
    stringToUTF8(src, ptr, length);
    setValue(retPtr, ptr, 'i32');

    return EmssCommon.Result.SUCCESS;
  },

  mediaElementSetSrc__deps: ['$EmssCommon', '$WasmHTMLMediaElement'],
  mediaElementSetSrc__proxy: 'sync',
  mediaElementSetSrc: function(handle, newSrc) {
    const mediaElement = WasmHTMLMediaElement.handleMap[handle];
    if (!mediaElement) {
      console.warn(`No such media element: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }
    try {
      mediaElement.src = UTF8ToString(newSrc);
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
    return EmssCommon.Result.SUCCESS;
  },

  mediaElementRegisterOnTimeUpdateEMSS__deps: ['$EmssCommon', '$WasmHTMLMediaElement', '$WasmElementaryMediaStreamSource'],
  mediaElementRegisterOnTimeUpdateEMSS__proxy: 'sync',
  mediaElementRegisterOnTimeUpdateEMSS: function(handle, sourceHandle, eventHandler, listener) {
    const mediaElement = WasmHTMLMediaElement.handleMap[handle];
    if (!mediaElement) {
      console.warn(`No such media element: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }

    const source = WasmElementaryMediaStreamSource.handleMap[sourceHandle];
    if (!source) {
      console.warn(`No such Source: '${sourceHandle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }

    if (mediaElement.emssTimeUpdateListener) {
      console.warn(`Listener already set for media element: '${handle}'`);
      return EmssCommon.Result.LISTENER_ALREADY_SET;
    }

    const firePlaybackPositionChanged = () => {
      // Looping doesn't work in legacy EMSS, so it's emulated by performing
      // seek to the beginning of media when playback position reaches
      // EMULATED_LOOP_TRESHOLD to media duration.
      const EMULATED_LOOP_TRESHOLD = 3.0;
      const newTime = mediaElement.currentTime;
      if (mediaElement.loop &&
          newTime >= mediaElement.duration - EMULATED_LOOP_TRESHOLD) {
        mediaElement.currentTime = 0;
        return;
      }
      {{{ makeDynCall('vif') }}} (eventHandler, listener, newTime);
    }

    const timeUpdateForPositionChangeEmulationCb = (event) => {
      if (mediaElement.seeking) {
        return;
      }
      firePlaybackPositionChanged();
    };

    const openForPositionChangeEmulationCb = (event, runningFromDefaultHandler) => {
      const sourceListeners = WasmElementaryMediaStreamSource.listenerMap[source];
      if (!runningFromDefaultHandler && sourceListeners &&
          sourceListeners['sourceopen']) {
        // If sourceopen is registered, then it will emit emulated running time
        // change event. This is needed to ensure order of events is correct.
        return;
      }
      firePlaybackPositionChanged();
    };

    source.emssOpenForPositionChangeEmulation =
        openForPositionChangeEmulationCb;
    source.addEventListener('sourceopen', openForPositionChangeEmulationCb);

    mediaElement.emssTimeUpdateListener =
        timeUpdateForPositionChangeEmulationCb;
    mediaElement.addEventListener('timeupdate',
                                  timeUpdateForPositionChangeEmulationCb);

    return EmssCommon.Result.SUCCESS;
  },

  mediaElementUnregisterOnTimeUpdateEMSS__deps: ['$EmssCommon', '$WasmHTMLMediaElement'],
  mediaElementUnregisterOnTimeUpdateEMSS__proxy: 'sync',
  mediaElementUnregisterOnTimeUpdateEMSS: function(handle, sourceHandle) {
    const mediaElement = WasmHTMLMediaElement.handleMap[handle];
    if (!mediaElement) {
      console.warn(`No such media element: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }

    if (!mediaElement.emssTimeUpdateListener) {
      console.warn(`Listener not registered for media element: '${handle}'`);
      return EmssCommon.Result.NO_SUCH_LISTENER;
    }

    mediaElement.removeEventListener('timeupdate',
                                     mediaElement.emssTimeUpdateListener);
    delete mediaElement.emssTimeUpdateListener;

    const source = WasmElementaryMediaStreamSource.handleMap[sourceHandle];
    if (!source) {
      console.warn(`No such Source: '${sourceHandle}'`);
    } else {
      mediaElement.removeEventListener('sourceopen',
          source.emssOpenForPositionChangeEmulation);
      delete source.emssOpenForPositionChangeEmulation;
    }

    return EmssCommon.Result.SUCCESS;
  },

  mediaElementPlay__deps: ['$WasmHTMLMediaElement'],
  mediaElementPlay__proxy: 'sync',
  mediaElementPlay: function(handle, onFinished, userData) {
    return WasmHTMLMediaElement._callAsyncFunction(
      handle, onFinished, userData, 'play');
  },

  mediaElementPause__deps: ['$EmssCommon', '$WasmHTMLMediaElement'],
  mediaElementPause__proxy: 'sync',
  mediaElementPause: function(handle) {
    const mediaElement = WasmHTMLMediaElement.handleMap[handle];
    if (!mediaElement) {
      console.warn(`No such media element: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }
    mediaElement.pause();
    return EmssCommon.Result.SUCCESS;
  },

  mediaElementSetOnError__deps: ['$EmssCommon','$WasmHTMLMediaElement'],
  mediaElementSetOnError__proxy: 'sync',
  mediaElementSetOnError: function(
      handle, eventHandler, userData) {
    const mediaElement = WasmHTMLMediaElement.handleMap[handle];
    if (!mediaElement) {
      console.warn(`No such media element: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }
    return WasmHTMLMediaElement._setListener(
      handle,
      'error',
      () => {
        const mediaError = mediaElement.error;
        const errorCode = mediaError.code;
        const errorMessage = mediaError.message;
        const length = lengthBytesUTF8(errorMessage) + 1;
        const errorMessagePtr = _malloc(length);
        stringToUTF8(errorMessage, errorMessagePtr, length);
        {{{ makeDynCall('viii') }}} (
          eventHandler, errorCode, errorMessagePtr, userData);
        _free(errorMessagePtr);
      });
  },

  mediaElementUnsetOnError__deps: ['$WasmHTMLMediaElement'],
  mediaElementUnsetOnError__proxy: 'sync',
  mediaElementUnsetOnError: function(handle) {
    return WasmHTMLMediaElement._unsetListener(
      handle,
      'error');
  },

/*============================================================================*/
/*= samsung::wasm::ElementaryMediaStreamSource impl:                         =*/
/*============================================================================*/

  $WasmElementaryMediaStreamSource__deps: ['$EmssCommon'],
  $WasmElementaryMediaStreamSource__postset: 'WasmElementaryMediaStreamSource.init();',
  $WasmElementaryMediaStreamSource: {
    init: function() {
      // Matches samsung::wasm::ElementaryMediaStreamSource::Mode
      const Mode = Object.freeze({
        NORMAL: 0,
        LOW_LATENCY: 1,
        VIDEO_TEXTURE: 2,
      });

      // Matches samsung::wasm::ElementaryMediaStreamSource::ReadyState
      const ReadyState = Object.freeze({
        DETACHED: 0,
        CLOSED: 1,
        OPEN_PENDING: 2,
        OPEN: 3,
        ENDED: 4,
      });

      // JS -> C++ conversion maps

      const STR_TO_MODE = new Map([
        ['normal',      Mode.NORMAL      ],
        ['low-latency', Mode.LOW_LATENCY ],
        ['video-texture', Mode.VIDEO_TEXTURE ],
      ]);

      const STR_TO_READY_STATE = new Map([
        ['detached',     ReadyState.DETACHED     ],
        ['closed',       ReadyState.CLOSED       ],
        ['open-pending', ReadyState.OPEN_PENDING ],
        ['open',         ReadyState.OPEN         ],
        ['ended',        ReadyState.ENDED        ],
      ]);

      WasmElementaryMediaStreamSource = {
        handleMap: [],
        listenerMap: {},
        _callFunction: function(handle, name, ...args) {
          return EmssCommon._callFunction(
            WasmElementaryMediaStreamSource.handleMap,
            handle,
            name,
            ...args);
        },
        _callAsyncFunction: function(
            handle, onFinishedCallback, userData, name, ...args) {
          return EmssCommon._callAsyncFunction(
            WasmElementaryMediaStreamSource.handleMap,
            handle,
            EmssCommon._exceptionToErrorCode,
            onFinishedCallback,
            userData,
            name,
            ...args);
        },
        _getProperty: function(handle, property, retPtr, type) {
          return EmssCommon._getProperty(
            WasmElementaryMediaStreamSource.handleMap,
            handle,
            property,
            retPtr,
            type);
        },
        _setProperty: function(handle, property, value) {
          return EmssCommon._setProperty(
            WasmElementaryMediaStreamSource.handleMap, handle, property, value);
        },
        _addTrack: function(handle, configPtr, retPtr, type) {
          const elementaryMediaStreamSource
            = WasmElementaryMediaStreamSource.handleMap[handle];
          if (!elementaryMediaStreamSource) {
            console.error(`No such elementary media stream source: '${handle}'`);
            return EmssCommon.Result.WRONG_HANDLE;
          }

          const config = EmssCommon._extractBaseConfig(configPtr);
          EmssCommon._extendConfigTo(type, config, configPtr);
          let track = null;
          try {
            track = WasmElementaryMediaStreamSource._getAddTrackFunction(
              type, elementaryMediaStreamSource)(config);
          } catch (error) {
            console.error(error.message);
            return EmssCommon._exceptionToErrorCode(error);
          }
          const trackHandle = track.trackId;
          WasmElementaryMediaTrack.handleMap[trackHandle] = track;
          WasmElementaryMediaTrack.listenerMap[trackHandle] = {};
          setValue(retPtr, trackHandle, 'i32');

          return EmssCommon.Result.SUCCESS;
        },
        _getAddTrackFunction: function(type, elementaryMediaStreamSource) {
          switch(type) {
            case 'video':
              return config => elementaryMediaStreamSource.addVideoTrack(config);
            case 'audio':
              return config => elementaryMediaStreamSource.addAudioTrack(config);
            default:
              console.error(`Invalid track type: ${type}`);
              return;
          }
        },
        _getPropertyString: function(handle, property, retPtr, type, transform) {
          const elementaryMediaStreamSource
            = WasmElementaryMediaStreamSource.handleMap[handle];
          if (!elementaryMediaStreamSource) {
            console.error(`No such elementary media stream source: '${handle}'`);
            return EmssCommon.Result.WRONG_HANDLE;
          }
          const answer = transform(elementaryMediaStreamSource[property]);
          setValue(retPtr, answer, type);
          return EmssCommon.Result.SUCCESS;
        },
        _stringToMode: function(input) {
          return (STR_TO_MODE.has(input) ? STR_TO_MODE.get(input) : -1);
        },
        _stringToReadyState: function(input) {
          return (STR_TO_READY_STATE.has(input) ?
              STR_TO_READY_STATE.get(input) : -1);
        },
        _setListener: function(handle, eventName, eventHandler) {
          return EmssCommon._setListener(
            WasmElementaryMediaStreamSource, handle, eventName, eventHandler);
        },
        _unsetListener: function(handle, eventName) {
          return EmssCommon._unsetListener(
            WasmElementaryMediaStreamSource, handle, eventName);
        },
      };
    },
  },

/*============================================================================*/
/*= samsung::wasm::ElementaryMediaStreamSource bindings:                     =*/
/*============================================================================*/

  EMSSCreate__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSCreate__proxy: 'sync',
  EMSSCreate: function(mode) {
    const elementaryMediaStreamSource = new tizentvwasm.ElementaryMediaStreamSource(
      ['normal', 'low-latency', 'video-texture'][mode]);
    const handle = WasmElementaryMediaStreamSource.handleMap.length;
    WasmElementaryMediaStreamSource.handleMap[handle]
      = elementaryMediaStreamSource;
    WasmElementaryMediaStreamSource.listenerMap[handle] = {};
    return handle;
  },

  EMSSRemove__deps: ['$EmssCommon', '$WasmElementaryMediaStreamSource'],
  EMSSRemove__proxy: 'sync',
  EMSSRemove: function(handle) {
    if (!(handle in WasmElementaryMediaStreamSource.handleMap)) {
      console.error(`No such elementary media stream source: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }
    const source = WasmElementaryMediaStreamSource.handleMap[handle];
    if (typeof source.destroy == 'function') {
      source.destroy();
    }
    EmssCommon._clearListeners(WasmElementaryMediaStreamSource, handle);
    delete WasmElementaryMediaStreamSource.handleMap[handle];
    delete WasmElementaryMediaStreamSource.listenerMap[handle];
    return EmssCommon.Result.SUCCESS;
  },

  EMSSCreateObjectURL__deps: ['$EmssCommon', '$WasmElementaryMediaStreamSource'],
  EMSSCreateObjectURL__proxy: 'sync',
  EMSSCreateObjectURL: function(handle, retPtr) {
    const elementaryMediaStreamSource
      = WasmElementaryMediaStreamSource.handleMap[handle];
    if (!elementaryMediaStreamSource) {
      console.error(`No such media element: '${strId}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }

    const src = URL.createObjectURL(elementaryMediaStreamSource).toString();
    const length = lengthBytesUTF8(src) + 1;
    const ptr = _malloc(length);
    stringToUTF8(src, ptr, length);
    setValue(retPtr, ptr, 'i32');

    return EmssCommon.Result.SUCCESS;
  },

  EMSSRevokeObjectURL__proxy: 'sync',
  EMSSRevokeObjectURL: function(url) {
    const urlString = UTF8ToString(url);
    URL.revokeObjectURL(urlString);
  },

  EMSSAddAudioTrack__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSAddAudioTrack__proxy: 'sync',
  EMSSAddAudioTrack: function(handle, configPtr, retPtr) {
    return WasmElementaryMediaStreamSource._addTrack(
      handle, configPtr, retPtr, 'audio');
  },

  EMSSAddVideoTrack__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSAddVideoTrack__proxy: 'sync',
  EMSSAddVideoTrack: function(handle, configPtr, retPtr) {
    return WasmElementaryMediaStreamSource._addTrack(
      handle, configPtr, retPtr, 'video');
  },

  EMSSRemoveTrack__deps: ['$EmssCommon', '$WasmElementaryMediaStreamSource'],
  EMSSRemoveTrack__proxy: 'sync',
  EMSSRemoveTrack: function(handle, trackHandle) {
    if (!(handle in WasmElementaryMediaStreamSource.handleMap)) {
      console.error(`No such ElementaryMediaStreamSource: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }
    if (!(trackHandle in WasmElementaryMediaTrack.handleMap)) {
      console.error(`No such ElementaryMediaTrack: '${trackHandle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }

    WasmElementaryMediaStreamSource.handleMap[handle].removeTrack(
      WasmElementaryMediaTrack.handleMap[trackHandle]);

    EmssCommon._clearListeners(WasmElementaryMediaTrack, trackHandle);
    delete WasmElementaryMediaTrack.handleMap[trackHandle];
    delete WasmElementaryMediaTrack.listenerMap[trackHandle];
    return EmssCommon.Result.SUCCESS;
  },

  EMSSFlush__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSFlush__proxy: 'sync',
  EMSSFlush: function(handle) {
    return WasmElementaryMediaStreamSource._callFunction(handle, 'flush');
  },

  EMSSClose__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSClose__proxy: 'sync',
  EMSSClose: function(handle, callback, userData) {
    return WasmElementaryMediaStreamSource._callAsyncFunction(
      handle, callback, userData, 'close');
  },

  EMSSOpen__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSOpen__proxy: 'sync',
  EMSSOpen: function(handle, callback, userData) {
    return WasmElementaryMediaStreamSource._callAsyncFunction(
      handle, callback, userData, 'open');
  },

  EMSSGetDuration__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSGetDuration__proxy: 'sync',
  EMSSGetDuration: function(handle, retPtr) {
    return WasmElementaryMediaStreamSource._getProperty(
      handle, 'duration', retPtr, 'double');
  },

  EMSSSetDuration__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSSetDuration__proxy: 'sync',
  EMSSSetDuration: function(handle, value) {
    return WasmElementaryMediaStreamSource._setProperty(
      handle, 'duration', value);
  },

  EMSSGetMode__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSGetMode__proxy: 'sync',
  EMSSGetMode: function(handle, retPtr) {
    return WasmElementaryMediaStreamSource._getPropertyString(
      handle, 'mode', retPtr, 'i32',
      WasmElementaryMediaStreamSource._stringToMode);
  },

  EMSSGetReadyState__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSGetReadyState__proxy: 'sync',
  EMSSGetReadyState: function(handle, retPtr) {
    return WasmElementaryMediaStreamSource._getPropertyString(
      handle, 'readyState', retPtr, 'i32',
      WasmElementaryMediaStreamSource._stringToReadyState);
  },

  EMSSSetOnPlaybackPositionChanged__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSSetOnPlaybackPositionChanged__proxy: 'sync',
  EMSSSetOnPlaybackPositionChanged: function(
      handle, eventHandler, userData) {
    return WasmElementaryMediaStreamSource._setListener(
      handle,
      'playbackpositionchanged',
      (event) => {
        {{{ makeDynCall('vfi') }}} (
          eventHandler, event.playbackPosition, userData);
      });
  },

  EMSSUnsetOnPlaybackPositionChanged__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSUnsetOnPlaybackPositionChanged__proxy: 'sync',
  EMSSUnsetOnPlaybackPositionChanged: function(handle) {
    return WasmElementaryMediaStreamSource._unsetListener(
      handle,
      'playbackpositionchanged');
  },

  EMSSSetOnSourceOpen__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSSetOnSourceOpen__proxy: 'sync',
  EMSSSetOnSourceOpen: function(handle, eventHandler, userData) {
    return WasmElementaryMediaStreamSource._setListener(
      handle,
      'sourceopen',
      (event) => {
        {{{ makeDynCall('vi') }}} (eventHandler, userData);

        // if running change emulation cb is registered, it needs to be emitted
        // here to assure order of events is correct.
        const source = WasmElementaryMediaStreamSource.handleMap[handle];
        if (!source) {
          return;
        }
        const openForPositionChangeEmulation =
            source.emssOpenForPositionChangeEmulation;
        if (openForPositionChangeEmulation) {
          openForPositionChangeEmulation(event, true);
        }
      });
  },

  EMSSUnsetOnSourceOpen__deps: ['$WasmElementaryMediaStreamSource'],
  EMSSUnsetOnSourceOpen__proxy: 'sync',
  EMSSUnsetOnSourceOpen: function(handle) {
    return WasmElementaryMediaStreamSource._unsetListener(
      handle,
      'sourceopen');
  },

/*============================================================================*/
/*= samsung::wasm::ElementaryMediaTrack impl:                                =*/
/*============================================================================*/

  $WasmElementaryMediaTrack__deps: ['$EmssCommon'],
  $WasmElementaryMediaTrack__postset: 'WasmElementaryMediaTrack.init();',
  $WasmElementaryMediaTrack: {
    init: function() {
      // Matches samsung::wasm::ElementaryMediaTrack::CloseReason
      const CloseReason = Object.freeze({
        SOURCE_CLOSED: 0,
        SOURCE_ERROR: 1,
        SOURCE_DETACHED: 2,
        TRACK_DISABLED: 3,
        TRACK_ENDED: 4,
        TRACK_SEEKING: 5,
        UNKNOWN: 6,
      });

      // JS -> C++ conversion maps

      const STR_TO_CLOSE_REASON = new Map([
        ['sourceclosed',   CloseReason.SOURCE_CLOSED   ],
        ['sourceerror',    CloseReason.SOURCE_ERROR    ],
        ['sourcedetached', CloseReason.SOURCE_DETACHED ],
        ['trackdisabled',  CloseReason.TRACK_DISABLED  ],
        ['trackended',     CloseReason.TRACK_ENDED     ],
        ['trackseeking',   CloseReason.TRACK_SEEKING   ],
        ['unknown',        CloseReason.UNKNOWN         ],
      ]);

      WasmElementaryMediaTrack = {
        handleMap: [],
        listenerMap: {},
        _callFunction: function(handle, name, ...args) {
          return EmssCommon._callFunction(
            WasmElementaryMediaTrack.handleMap,
            handle,
            name,
            ...args);
        },
        _callAsyncFunction: function(
            handle, onFinished, userData, name, ...args) {
          return EmssCommon._callAsyncFunction(
            WasmElementaryMediaTrack.handleMap,
            handle,
            EmssCommon._exceptionToErrorCode,
            onFinished,
            userData,
            name,
            ...args);
        },
        _getProperty: function(handle, property, retPtr, type) {
          return EmssCommon._getProperty(
            WasmElementaryMediaTrack.handleMap,
            handle,
            property,
            retPtr,
            type);
        },
        _setListener: function(handle, eventName, eventHandler) {
          return EmssCommon._setListener(
            WasmElementaryMediaTrack, handle, eventName, eventHandler);
        },
        _setProperty: function(handle, property, value) {
          return EmssCommon._setProperty(
            WasmElementaryMediaTrack.handleMap, handle, property, value);
        },
        _stringToCloseReason: function(input) {
          return (STR_TO_CLOSE_REASON.has(input)
              ? STR_TO_CLOSE_REASON.get(input)
              : CloseReason.UNKNOWN);
        },
        _unsetListener: function(handle, eventName) {
          return EmssCommon._unsetListener(
            WasmElementaryMediaTrack, handle, eventName);
        },
      };
    },
  },

/*============================================================================*/
/*= samsung::wasm::ElementaryMediaTrack bindings:                            =*/
/*============================================================================*/

  elementaryMediaTrackRemove__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackRemove__proxy: 'sync',
  elementaryMediaTrackRemove: function(handle) {
    if (!(handle in WasmElementaryMediaTrack.handleMap)) {
      console.error(`No such elementary media track: '${handle}'`);
      return EmssCommon.Result.WRONG_HANDLE;
    }
    EmssCommon._clearListeners(WasmElementaryMediaTrack, handle);
    delete WasmElementaryMediaTrack.handleMap[handle];
    delete WasmElementaryMediaTrack.listenerMap[handle];
    return EmssCommon.Result.SUCCESS;
  },

  elementaryMediaTrackAppendPacket__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackAppendPacket: function(handle, packetPtr) {
    try {
      const packet = EmssCommon._makePacketFromPtr(packetPtr);
      const data = EmssCommon._makePacketDataFromPtr(packetPtr);

      tizentvwasm.SideThreadElementaryMediaTrack.appendPacketSync(
            handle, packet, data);
      return EmssCommon.Result.SUCCESS;
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },

  elementaryMediaTrackAppendPacketAsync__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackAppendPacketAsync: function(handle, packetPtr) {
    try {
      const packet = EmssCommon._makePacketFromPtr(packetPtr);
      const data = EmssCommon._makePacketDataFromPtr(packetPtr);

      tizentvwasm.SideThreadElementaryMediaTrack.appendPacketAsync(
            handle, packet, data);
      return EmssCommon.Result.SUCCESS;
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },

  elementaryMediaTrackAppendEncryptedPacket__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackAppendEncryptedPacket: function(handle, packetPtr) {
    try {
      const packet = EmssCommon._makePacketFromPtr(packetPtr);
      EmssCommon._extendPacketToEncrypted(packet, packetPtr);
      const data = EmssCommon._makePacketDataFromPtr(packetPtr);

      tizentvwasm.SideThreadElementaryMediaTrack.appendPacketSync(
            handle, packet, data);
      return EmssCommon.Result.SUCCESS;
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },

  elementaryMediaTrackAppendEncryptedPacketAsync__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackAppendEncryptedPacketAsync: function(handle, packetPtr) {
    try {
      const packet = EmssCommon._makePacketFromPtr(packetPtr);
      EmssCommon._extendPacketToEncrypted(packet, packetPtr);
      const data = EmssCommon._makePacketDataFromPtr(packetPtr);

      tizentvwasm.SideThreadElementaryMediaTrack.appendPacketAsync(
            handle, packet, data);
      return EmssCommon.Result.SUCCESS;
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },

  elementaryMediaTrackAppendEndOfTrack__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackAppendEndOfTrack: function(handle, sessionId) {
    try {
      if (sessionId !== EmssCommon.IGNORE_SESSION_ID) {
        tizentvwasm.SideThreadElementaryMediaTrack.appendEndOfTrackSync(
            handle, sessionId);
      } else {
        tizentvwasm.SideThreadElementaryMediaTrack.appendEndOfTrackSync(handle);
      }
      return EmssCommon.Result.SUCCESS;
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },

  elementaryMediaTrackAppendEndOfTrackAsync__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackAppendEndOfTrackAsync: function(handle, sessionId) {
    try {
      if (sessionId !== EmssCommon.IGNORE_SESSION_ID) {
        tizentvwasm.SideThreadElementaryMediaTrack.appendEndOfTrackAsync(
            handle, sessionId);
      } else {
        tizentvwasm.SideThreadElementaryMediaTrack.appendEndOfTrackAsync(handle);
      }
      return EmssCommon.Result.SUCCESS;
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },


  elementaryMediaTrackFillTextureWithNextFrame__deps: ['$EmssCommon', '$GL'],
  elementaryMediaTrackFillTextureWithNextFrame__proxy: 'sync',
  elementaryMediaTrackFillTextureWithNextFrame: function(
      handle, textureId, onFinished, userData) {
    const webGLTexture = GL.textures[textureId];
    try {
      return WasmElementaryMediaTrack._callAsyncFunction(
        handle, onFinished, userData, 'getPicture', webGLTexture);
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },

  elementaryMediaTrackGetSessionId__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackGetSessionId__proxy: 'sync',
  elementaryMediaTrackGetSessionId: function(handle, retPtr) {
    return WasmElementaryMediaTrack._getProperty(
      handle, 'sessionId', retPtr, 'i32');
  },

  elementaryMediaTrackIsOpen__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackIsOpen__proxy: 'sync',
  elementaryMediaTrackIsOpen: function(handle, retPtr) {
    return WasmElementaryMediaTrack._getProperty(
      handle, 'isOpen', retPtr, 'i8');
  },

  elementaryMediaTrackRecycleTexture__deps: ['$EmssCommon', '$GL'],
  elementaryMediaTrackRecycleTexture__proxy: 'sync',
  elementaryMediaTrackRecycleTexture: function(handle, textureId) {
    const webGLTexture = GL.textures[textureId];
    const videoPicture = {
      "texture": webGLTexture,
      "textureTarget": 0x8D65  // GL_TEXTURE_EXTERNAL_OES
    };

    try {
      return WasmElementaryMediaTrack._callFunction(
        handle, 'recyclePicture', videoPicture);
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },

  elementaryMediaTrackRegisterCurrentGraphicsContext__deps: ['$EmssCommon', '$GL'],
  elementaryMediaTrackRegisterCurrentGraphicsContext__proxy: 'sync',
  elementaryMediaTrackRegisterCurrentGraphicsContext: function(handle) {
    const webGLContext = GL.currentContext.GLctx;
    try {
      return WasmElementaryMediaTrack._callFunction(
        handle, 'setWebGLRenderingContext', webGLContext);
    } catch (error) {
      console.error(error.message);
      return EmssCommon._exceptionToErrorCode(error);
    }
  },

  elementaryMediaTrackSetMediaKey__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackSetMediaKey__proxy: 'sync',
  elementaryMediaTrackSetMediaKey: function(handle, mediaKeysHandle) {
    const mediaKeys = EmssMediaKey.handleMap[mediaKeysHandle];
    if (!mediaKeys) {
      return EmssCommon.Result.WRONG_HANDLE;
    }
    return WasmElementaryMediaTrack._callFunction(
      handle, 'setMediaKeySession', mediaKeys.mediaKeySession);
  },

  elementaryMediaTrackSetOnAppendError__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackSetOnAppendError__proxy: 'sync',
  elementaryMediaTrackSetOnAppendError: function(
      handle, eventHandler, userData) {
    return WasmElementaryMediaTrack._setListener(
      handle,
      'appenderror',
      (event) => {
        const appendError = event.error;
        const asyncAppendResult = EmssCommon._exceptionToErrorCode(appendError);
        {{{ makeDynCall('vii') }}} (eventHandler, asyncAppendResult, userData);
      });
  },

  elementaryMediaTrackUnsetSetOnAppendError__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackUnsetSetOnAppendError__proxy: 'sync',
  elementaryMediaTrackUnsetSetOnAppendError: function(handle) {
    return WasmElementaryMediaTrack._unsetListener(
      handle,
      'appenderror');
  },

  elementaryMediaTrackSetOnTrackClosed__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackSetOnTrackClosed__proxy: 'sync',
  elementaryMediaTrackSetOnTrackClosed: function(
      handle, eventHandler, userData) {
    return WasmElementaryMediaTrack._setListener(
      handle,
      'trackclosed',
      (event) => {
        const closeReason =
            WasmElementaryMediaTrack._stringToCloseReason(event.reason);
        {{{ makeDynCall('vii') }}} (
          eventHandler,
          closeReason,
          userData);
        // if trackclosed_sid_emulation is registered, it needs to be emitted
        // here to assure events order is correct.
        const onClosedForSessionEmulation =
            WasmElementaryMediaTrack.listenerMap[handle][
                'trackclosed_sid_emulation'];
        if (onClosedForSessionEmulation) {
          onClosedForSessionEmulation(event, true);
        }
      });
  },

  elementaryMediaTrackUnsetOnTrackClosed__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackUnsetOnTrackClosed__proxy: 'sync',
  elementaryMediaTrackUnsetOnTrackClosed: function(handle) {
    return WasmElementaryMediaTrack._unsetListener(
      handle,
      'trackclosed');
  },

  elementaryMediaTrackSetOnSeek__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackSetOnSeek__proxy: 'sync',
  elementaryMediaTrackSetOnSeek: function(
      handle, eventHandler, userData) {
    return WasmElementaryMediaTrack._setListener(
      handle,
      'seek',
      (event) => {
        {{{ makeDynCall('vfi') }}} (eventHandler, event.newTime, userData);
      });
  },

  elementaryMediaTrackUnsetOnSeek__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackUnsetOnSeek__proxy: 'sync',
  elementaryMediaTrackUnsetOnSeek: function(handle) {
    return WasmElementaryMediaTrack._unsetListener(
      handle,
      'seek');
  },

  elementaryMediaTrackSetOnSessionIdChanged__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackSetOnSessionIdChanged__proxy: 'sync',
  elementaryMediaTrackSetOnSessionIdChanged: function(
      handle, eventHandler, userData) {
    return WasmElementaryMediaTrack._setListener(
      handle,
      'sessionidchanged',
      (event) => {
        {{{ makeDynCall('vii') }}} (eventHandler, event.sessionId, userData);
      });
  },

  elementaryMediaTrackUnsetOnSessionIdChanged__deps: ['$WasmElementaryMediaTrack'],
  elementaryMediaTrackUnsetOnSessionIdChanged__proxy: 'sync',
  elementaryMediaTrackUnsetOnSessionIdChanged: function(handle) {
    return WasmElementaryMediaTrack._unsetListener(
      handle,
      'sessionidchanged');
  },

  elementaryMediaTrackSetListenersForSessionIdEmulation__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackSetListenersForSessionIdEmulation__proxy: 'sync',
  elementaryMediaTrackSetListenersForSessionIdEmulation: function(
      handle, closedHandler, userData) {
    console.info(
        `session_id will be emulated for track ${handle}, for object: ${userData}`);

    const onClosed = (event, runningFromDefaultHandler) => {
      if (!runningFromDefaultHandler &&
          WasmElementaryMediaTrack.listenerMap[handle]['trackclosed']) {
        // If trackclosed is registered, then it will emit emulated session
        // change event. This is needed to ensure order of events is correct.
        return;
      }
      {{{ makeDynCall('vii') }}} (
        closedHandler,
        WasmElementaryMediaTrack._stringToCloseReason(event.reason),
        userData);
    };

    const obj = WasmElementaryMediaTrack.handleMap[handle];
    if (obj) {
      WasmElementaryMediaTrack.listenerMap[handle][
          'trackclosed_sid_emulation'] = onClosed;
      obj.addEventListener('trackclosed', onClosed);
    } else {
      console.warn(`No such Track: '${handle}'`);
    }
    return EmssCommon.Result.SUCCESS;
  },

  elementaryMediaTrackUnsetListenersForSessionIdEmulation__deps: ['$EmssCommon', '$WasmElementaryMediaTrack'],
  elementaryMediaTrackUnsetListenersForSessionIdEmulation__proxy: 'sync',
  elementaryMediaTrackUnsetListenersForSessionIdEmulation: function(handle) {
    const obj = WasmElementaryMediaTrack.handleMap[handle];
    obj.removeEventListener('trackclosed', WasmElementaryMediaTrack.listenerMap[
        handle]['trackclosed_sid_emulation']);
    WasmElementaryMediaTrack.listenerMap[handle]['trackclosed_sid_emulation'] =
        null;
    return EmssCommon.Result.SUCCESS;
  },

/*============================================================================*/
/*= Bindings for listeners' setters and unsetters:                           =*/
/*============================================================================*/

  {{{
    const makeEventHandlerFor = (objName, wasmImplName) => (eventName) => {
      return [
        `${objName}Set${eventName}__deps: ['$${wasmImplName}'],`,
        `${objName}Set${eventName}__proxy: 'sync',`,
        `${objName}Set${eventName}: function(`,
        `    handle, eventHandler, userData) {`,
        `  return ${wasmImplName}._setListener(`,
        `    handle,`,
        `    '${eventName.toLowerCase().slice(2)}',`,
        `    () => dynCall('vi', eventHandler, [userData]));`,
        `},`,
        ``,
        `${objName}Unset${eventName}__deps: ['$${wasmImplName}'],`,
        `${objName}Unset${eventName}__proxy: 'sync',`,
        `${objName}Unset${eventName}: function(handle) {`,
        `  return ${wasmImplName}._unsetListener(`,
        `    handle,`,
        `    '${eventName.toLowerCase().slice(2)}');`,
        `},`,
      ].join('\n');
    };

    modifyFunction(
      "function _() {}",
      () => {
        const mediaElementHandlers = [
          'OnPlaying',
          'OnTimeUpdate',
          'OnLoadStart',
          'OnLoadedMetadata',
          'OnLoadedData',
          'OnCanPlay',
          'OnCanPlayThrough',
          'OnEnded',
          'OnPlay',
          'OnSeeking',
          'OnSeeked',
          'OnPause',
          'OnWaiting'];
        const EMSSHandlers = [
          'OnSourceDetached',
          'OnSourceClosed',
          'OnSourceOpenPending',
          'OnSourceEnded'];
        const elementaryMediaTrackHandlers = [
          'OnTrackOpen'];

        return mediaElementHandlers
          .map(makeEventHandlerFor('mediaElement',
                                   'WasmHTMLMediaElement'))
          .concat(EMSSHandlers
            .map(makeEventHandlerFor('EMSS',
                                     'WasmElementaryMediaStreamSource')))
          .concat(elementaryMediaTrackHandlers
            .map(makeEventHandlerFor('elementaryMediaTrack',
                                     'WasmElementaryMediaTrack')))
          .join('\n');
      });
  }}}
}; // LibraryTizenEmss

/*============================================================================*/
/*= Add to LibraryManager:                                                   =*/
/*============================================================================*/

mergeInto(LibraryManager.library, LibraryTizenEmss);
