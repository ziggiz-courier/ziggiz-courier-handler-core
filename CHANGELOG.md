# CHANGELOG


## v0.4.0 (2025-05-23)

### Features

- Additional spans
  ([`cfa689b`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/cfa689b898c4cbc105c973887215f6ae01a67acc))


## v0.3.0 (2025-05-23)

### Features

- Add basic spans
  ([`58635a5`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/58635a5beaa9786cb800208608b4da734945e1e9))

- New modules for Connection to be used
  ([`74df307`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/74df307a6dc9df7e148f17ba24fddb639007dd7a))


## v0.2.3 (2025-05-23)

### Bug Fixes

- Correct storage of org and product
  ([`eb5180d`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/eb5180d696668dae2770a4de01f9303c62fa6c53))


## v0.2.2 (2025-05-23)

### Bug Fixes

- Build typo
  ([`13c4f8a`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/13c4f8aa9d1d41c93726b75d57391667f2d676a1))


## v0.2.1 (2025-05-23)

### Bug Fixes

- Remove unused prompts
  ([`1de9e4f`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/1de9e4f6de87c8fa6e34f545032eebfd1032a6a3))

- Tests alone don't need releases
  ([`09462ce`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/09462ce1bec3c2a7224f1bdeacdedb5cf7386256))

### Chores

- Update releaseer
  ([`7011fdd`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/7011fddab9f215330d3b25ad08080bbda1c5dea6))

### Continuous Integration

- Correct test matrix
  ([`918ffa0`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/918ffa09f35646b355c85247002d7c9e3ed98632))

- Coverage
  ([`f89f10a`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/f89f10a01a13060c48e6799a4b2451684dde2b7b))

- Fix
  ([`593f9f8`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/593f9f86fee05e67c9bff43644d51502171140bc))

- Updates for tox
  ([`da6e66d`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/da6e66d7a7d42de26eb14bc60036707c0c0703d2))


## v0.2.0 (2025-05-23)

### Bug Fixes

- Address cases where there are no fields
  ([`fb9718b`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/fb9718b4c9bc21dca2406188ea80e7cfe99dd00e))

- Address mypy reports
  ([`8e8d059`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/8e8d059e87393376de3ba080061e0d6b7e74505f))

- Correct default pri
  ([`e34109b`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/e34109b494ce11f957ee7e3390602dbb2e526918))

- Handle storage of vendor and product properly
  ([`492e74c`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/492e74cf7d8ffda10032ec239690e0ffc55468c1))

- Issues reported as PEP 484
  ([`c5085b1`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/c5085b1f86fc66dd732941ee7b4a46fe535ce68c))

- Leef to issues
  ([`26232e5`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/26232e57a9a66f5904b2800e073800806600a439))

- Mypy errors
  ([`626acf2`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/626acf21cb5022b73290f536784d799fd3201d17))

- Mypy errors with DATE_FORMATS constant
  ([`5adf31a`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/5adf31a000af55c5b60848cf8fa95f8a5a1ebcc9))

- Mypy issue where timestamp was not Optional as it should be
  ([`f4c8579`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/f4c857994ea9a1f86b5f497a171c2e353a20ab77))

- Mypy issues
  ([`33b3188`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/33b318881a6824d1afa3794540a967204cc362e1))

- Remove hard coded test cheat
  ([`b0d6ff3`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/b0d6ff3f14eb51193aa5c1dbc5fc0ad7f6cc7433))

- Return None instead of raising value error exceptions for performance
  ([`426b236`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/426b23680c05d4579eb2e7f109006bc40bd9ec4a))

- **types**: Add type ignore comments for SourceProducer assignments in parsers
  ([`e52c334`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/e52c334f165d285efae671ed44e041adc2adcafc))

- **types**: Resolve mypy errors in base.py, paloalto plugin, and otel_encoder
  ([`21fc6e7`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/21fc6e74554c922422e10cf23a27b526af870908))

- **types**: Use typing.cast to resolve return type issues in parsers
  ([`71cb9b7`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/71cb9b7b4924c1b5e25a5d0aab8e95b4dcecbc24))

### Chores

- Additional mypy fixes
  ([`8786b48`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/8786b48d68469b2aa2be68952dbb897c770cc5fb))

- Cleanup cef
  ([`25eb06c`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/25eb06cee4befc053cbf1310ac5b736ae9710f01))

- Correct license header
  ([`d27174f`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/d27174f5efae05c658c8b4935504754fef79c009))

- Fix license headers
  ([`6da57d8`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/6da57d83999840d75ae53da562a2ec7fc5c43351))

- Remove parse_leef1_message
  ([`e3f2c2d`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/e3f2c2dac9182e7fa46d0dd7bbd97ac2c1424463))

- Test with tox
  ([`dac2e73`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/dac2e73cf37a13f79de39a06874c88086c5b297c))

### Features

- Provide a method for message parser cache handling
  ([`7dc06a0`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/7dc06a0e77e179839855d31490db4ea5d920373e))

### Refactoring

- Add ABC for message parsing
  ([`1c2bb83`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/1c2bb835da9850b6738c97e4579acc9c836c12ef))

- Move message parsers to their own folder in utils
  ([`c73821f`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/c73821fa690a3db520b284e896b0414570c9a52f))

- Tests new folder
  ([`c4873db`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/c4873db91d0c41b123a0ddcd8bb76da236b098b0))

### Testing

- Fix mypy issues
  ([`2ac347a`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/2ac347a8b4c4c2045fbe973e899ecca3e1958e52))


## v0.1.1 (2025-05-21)

### Bug Fixes

- **RFC5424**: Version must be 1
  ([`a1a5c78`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/a1a5c784cbb4d57cc0e9e88e274d2ec4aa50a4e1))


## v0.1.0 (2025-05-19)

### Chores

- Cleanup with precommit
  ([`fee82df`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/fee82df7e1f81c4735e62ff445f05a7f8a8a5111))

### Continuous Integration

- Fix cache issue
  ([`23b25e7`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/23b25e77d30a2ba640b36916c95e872dddb12255))

- Fix path
  ([`0988955`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/09889554f977f91886e5bb3972b544ac2b5c4209))

- Fix poetry
  ([`cb336fe`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/cb336fe307af9a5857d52964694cdf6bfdadacb9))

- Fix poetry
  ([`ad52d1e`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/ad52d1e87fec80f8d6fafda9362f17c4a9c3f5b9))

- Fix poettry
  ([`f6b774d`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/f6b774d1f27496da6392f517e3e78880a02beaf9))

### Documentation

- **readme,developing**: Update documentation for code structure, standards, and extension
  guidelines
  ([`2e96d4d`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/2e96d4da0bc8a7a20d797aa3413e775e8c4764dd))

### Features

- Initial Commit
  ([`9ef3e3f`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/9ef3e3f2a4864b309c2e412509e7d7255cfe6e7d))

- Prepare for python 3.15 date parsing
  ([`f0721f6`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/f0721f67afb18125b1ecf71c34115c67646e4a92))

### Refactoring

- Better location for org and product
  ([`bd627df`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/bd627df0b06e726ecb2b06fdaa0e77592701b812))

- Complete refactor to org and product
  ([`95f7192`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/95f719275a9d4bdf994aa86f91ba404dc55af8d0))

- Correct class name
  ([`b84d295`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/b84d29535ba8b138e66d246891765e0b725395a7))

- Use correct param
  ([`1528719`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/152871965d16b0bc85b05c8c7c3f21d2e334e2d8))

### Testing

- Organize test cases in classes
  ([`f4dd4fe`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/f4dd4fe1a851212b6b9b3109293f62933136ee6f))

- Refactor for sp validation
  ([`9240db5`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/9240db5e7b4be6fffa836ad915b8983ce333b67e))

- Refactor tests to be more dry
  ([`9aeb3b9`](https://github.com/ziggiz-courier/ziggiz-courier-handler-core/commit/9aeb3b94f45f0376bd2926af282d3dab269a7f56))
