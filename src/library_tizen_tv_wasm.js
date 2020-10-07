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

    getLegacyWasmPlayerVersion: function() {
      if (tizentvwasm.ElementaryMediaStreamSource) {
        if (tizentvwasm.ElementaryMediaTrack.prototype.hasOwnProperty(
            'sessionId')) {
          return {
            name: 'ElementaryMediaStreamSource',
            version: '0.9',
            apiLevels: [1],
            features: ['base-emss'],
          };
        } else {
          return {
            name: 'ElementaryMediaStreamSource',
            version: '0.1',
            apiLevels: [0],
            features: ['legacy-emss'],
          };
        }
      }
      return null;
    },

    getLegacyWasmSocketsVersion: function() {
      return {
        name: 'TizenSockets',
        version: '1.0',
        apiLevels: [1],
        features: [],
      };
    },

    getLegacyApis: function() {
      const legacyApis = [
        TIZENTVWASM.getLegacyWasmSocketsVersion(),
      ];
      const legacyEmss = TIZENTVWASM.getLegacyWasmPlayerVersion();
      if (legacyEmss) {
        legacyApis.push(legacyEmss);
      }
      return legacyApis;
    },

    getAvailableApis: function() {
      const hasAvailableApis =
          (typeof tizentvwasm.availableApis !== 'undefined');
      const hasApiFeatureSupported =
          (typeof tizentvwasm.isApiFeatureSupported !== 'undefined');

      const availableApis = hasAvailableApis ?
        tizentvwasm.availableApis : TIZENTVWASM.getLegacyApis();

      // Polyfill `features` key if we're on platform it's not supported:
      if (hasAvailableApis && !hasApiFeatureSupported) {
        availableApis.forEach((apiInfo) => {
          if (apiInfo.name === 'ElementaryMediaStreamSource') {
            apiInfo.features = ['base-emss'];
            if (apiInfo.apiLevels.includes(2)) {
              apiInfo.features.push('video-texture');
            }
            if (apiInfo.apiLevels.includes(3)) {
              apiInfo.features.push('software-decoding');
            }
            return;
          }
          // Only WASM Player had any features that could be emulated before
          // isApiFeatureSupported() API was added.
          apiInfo.features = [];
        });
      }

      return availableApis;
    },
  },

  TizenTVWasm_GetAvailableApis__deps: ['$TIZENTVWASM'],
  TizenTVWasm_GetAvailableApis__sig: 'viiii',
  TizenTVWasm_GetAvailableApis: function(
    addFeatureCb, addApiInfoCb, featuresPtr, apiInfoPtr) {
    if (!TIZENTVWASM.hasTizenTVWasm()) {
      console.error('Not a TizenTV device?');
      return;
    }

    const addResult = function(apiInfo) {
      if (!apiInfo) return;

      // Populate features
      apiInfo.features.forEach((feature) => {
        const featurePtr = TIZENTVWASM.allocCStr(feature);
        try {
          dynCall('vii', addFeatureCb, [featurePtr, featuresPtr]);
        } catch (error) {
          console.error(error);
        } finally {
          _free(featurePtr);
        }
      });

      // Populate api info
      const namePtr = TIZENTVWASM.allocCStr(apiInfo.name);
      const versionPtr = TIZENTVWASM.allocCStr(apiInfo.version);
      const levelsPtr = _malloc(apiInfo.apiLevels.byteLength);
      try {
        for (let i = 0; i != apiInfo.apiLevels.length; i++) {
          setValue(levelsPtr + (i * 4), apiInfo.apiLevels[i], 'i32');
        }
        dynCall('viiiiii', addApiInfoCb, [
          namePtr, versionPtr, levelsPtr, apiInfo.apiLevels.length,
          featuresPtr, apiInfoPtr,
        ]);
      } catch (error) {
        console.error(error);
      } finally {
        _free(namePtr);
        _free(versionPtr);
        _free(levelsPtr);
      }
    };

    TIZENTVWASM.getAvailableApis().forEach(addResult);
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
    if (typeof tizentvwasm.isApiSupported !== 'undefined') {
      return (tizentvwasm.isApiSupported(apiName, apiLevel) ? 1 : 0);
    } else {
      const legacyApis = TIZENTVWASM.getAvailableApis();
      for (const api of legacyApis) {
        if (api.name == apiName && api.apiLevels.includes(apiLevel)) {
          return 1;
        }
      }
      return 0;
    }
  },

  TizenTVWasm_IsApiFeatureSupported__deps: ['$TIZENTVWASM'],
  TizenTVWasm_IsApiFeatureSupported__sig: 'iii',
  TizenTVWasm_IsApiFeatureSupported: function(apiNamePtr, featurePtr) {
    if (!TIZENTVWASM.hasTizenTVWasm()) {
      console.error('Not a TizenTV device?');
      return 0;
    }
    const apiName = UTF8ToString(apiNamePtr);
    const feature = UTF8ToString(featurePtr);
    if (typeof tizentvwasm.isApiFeatureSupported !== 'undefined') {
      return (tizentvwasm.isApiFeatureSupported(apiName, feature) ? 1 : 0);
    } else {
      const legacyApis = TIZENTVWASM.getAvailableApis();
      for (const api of legacyApis) {
        if (api.name == apiName && api.features.includes(feature)) {
          return 1;
        }
      }
      return 0;
    }
  },
};

mergeInto(LibraryManager.library, LibraryTizenTVWasm);
