// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

const LibraryTizenTVWasm = {
  $TIZENTVWASM: {
    hasTizenTVWasm: function() {
      return (typeof tizentvwasm !== 'undefined');
    },

    allocCStr: function(jsString) {
      const length = lengthBytesUTF8(jsString) + 1;
      const ptr = _malloc(length);
      stringToUTF8(jsString, ptr, length);
      return ptr;
    },
  },

  TizenTVWasm_GetAvailableApis__deps: ['$TIZENTVWASM'],
  TizenTVWasm_GetAvailableApis__sig: 'vii',
  TizenTVWasm_GetAvailableApis: function(callback, userData) {
    if (!TIZENTVWASM.hasTizenTVWasm()) {
      console.error('Not a TizenTV device?');
      return;
    }
    tizentvwasm.availableApis.forEach(function(apiInfo) {
      const namePtr = TIZENTVWASM.allocCStr(apiInfo.name);
      const versionPtr = TIZENTVWASM.allocCStr(apiInfo.version);
      const levelsPtr = _malloc(apiInfo.apiLevels.byteLength);
      try {
        for (var i = 0; i != apiInfo.apiLevels.length; i++) {
          setValue(levelsPtr + i, apiInfo.apiLevels[i], 'i32');
        }
        dynCall('viiiii', callback, [
          namePtr, versionPtr, levelsPtr, apiInfo.apiLevels.length, userData
        ]);
      } catch (error) {
        console.error(error);
      } finally {
        _free(namePtr);
        _free(versionPtr);
        _free(levelsPtr);
      }
    });
  },

  TizenTVWasm_GetSupportedInstructions__deps: ['$TIZENTVWASM'],
  TizenTVWasm_GetSupportedInstructions__sig: 'vii',
  TizenTVWasm_GetSupportedInstructions: function(callback, userData) {
    if (!TIZENTVWASM.hasTizenTVWasm()) {
      console.error('Not a TizenTV device?');
      return;
    }
    tizentvwasm.supportedInstructions().forEach(function(instructionSet) {
      const instructionSetPtr = TIZENTVWASM.allocCStr(instructionSet);
      try {
        dynCall('vii', callback, [instructionSetPtr, userData]);
      } catch (error) {
        console.error(error);
      } finally {
        _free(instructionSetPtr);
      }
    });
  },

  TizenTVWasm_IsApiSupported__deps: ['$TIZENTVWASM'],
  TizenTVWasm_IsApiSupported__sig: 'iii',
  TizenTVWasm_IsApiSupported: function(apiNamePtr, apiLevel) {
    if (!TIZENTVWASM.hasTizenTVWasm()) {
      console.error('Not a TizenTV device?');
      return 0;
    }
    const apiName = UTF8ToString(apiNamePtr);
    return (tizentvwasm.isApiSupported(apiName, apiLevel) ? 1 : 0);
  },

};

mergeInto(LibraryManager.library, LibraryTizenTVWasm);
