# CHANGELOG

<!-- version list -->

## v0.22.0 (2026-08-28)

### Bug Fixes

- Handle fetch target not found errors
  ([#89](https://github.com/LinkupPlatform/linkup-python-sdk/pull/89),
  [`d621384`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/d6213840fb0dcbdfb783bf3e4794e6c321eed27e))

### Chores

- Remove cross field valition from SDK
  ([`249fdd0`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/249fdd0b1cc6f3b347f0779dcb831a7e438ae174))

### Features

- Support structured fetch extraction
  ([`e927e75`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/e927e75bef4944cb23faba2b9d68f02518925156))


## v0.21.0 (2026-08-18)

### Chores

- Update lock file dependencies
  ([`be653ff`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/be653ffe73bd34d8f0430878ca1e27a8086fc50c))

### Features

- Support fetch mode selection
  ([`b9d06fb`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/b9d06fbca88f06f78c9fe903f05c50706ddbf0bb))


## v0.20.0 (2026-08-05)

### Features

- Expose fetch favicon
  ([`f34440a`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/f34440acbf6c3438b914c2de91d73e1182bccb31))


## v0.19.1 (2026-08-04)

### Bug Fixes

- Expose ip whitelist errors
  ([`8da5590`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/8da55901d3408d51f29e8befdc54d252600e9a6c))


## v0.19.0 (2026-07-29)

### Features

- Support raw content fetch responses
  ([#85](https://github.com/LinkupPlatform/linkup-python-sdk/pull/85),
  [`ef3ece8`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/ef3ece8c06ac4c0a573ac4441d957f51a87199b6))


## v0.18.4 (2026-07-29)

### Bug Fixes

- Handle fetch target unreachable errors
  ([#84](https://github.com/LinkupPlatform/linkup-python-sdk/pull/84),
  [`5f4ed40`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/5f4ed40f193b58d364848b70a7d918490f0b3c99))


## v0.18.3 (2026-06-30)

### Bug Fixes

- Handle unsupported task types
  ([`d9a9a13`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/d9a9a13594528b305bc1f22cabc94dd26655a919))

### Documentation

- Fix missing status code in error docstring
  ([`ca0422c`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/ca0422caa67edf2734ed06f2e03c5b843b99b2d4))


## v0.18.2 (2026-06-04)

### Bug Fixes

- More validation in models
  ([`4ff43f0`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/4ff43f0c6a4e5294ee54f93e0669e6ed8f0ff16b))

### Chores

- Remove inconsistent backticks in docstrings
  ([`4109b65`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/4109b65202561f912b4bb5eead1210ffaa455b7f))

- Setup scratch file directory
  ([`83beb9f`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/83beb9fbfc81d3840afb3bbb558ffef5c89dfdeb))

- Simplify setup of datetime module
  ([`b35d430`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/b35d4303954c7b3f28e19cf95bb7ba82eae5091b))

- Upgrade deps with vulnerabilities
  ([`4ffeb99`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/4ffeb99c426271090d4e3dfcec17a12891b81969))


## v0.18.1 (2026-06-03)

### Bug Fixes

- Validate structured research input before request
  ([`65676c2`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/65676c2131f063291edf01cc0950b420ebe8fbdb))


## v0.18.0 (2026-06-01)

### Bug Fixes

- Always return structured outputs as dicts
  ([`0cded9d`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/0cded9d998f9e9df8ad5781fd0a7b4abf1fa16a0))


## v0.17.1 (2026-06-01)

### Bug Fixes

- Allow to use string dates directly
  ([`7b64243`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/7b64243d36c42fa31766edc0d307999b8380a591))


## v0.17.0 (2026-05-29)

### Features

- **client**: Add custom auth header name support
  ([#75](https://github.com/LinkupPlatform/linkup-python-sdk/pull/75),
  [`434751e`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/434751ee654da434a6ce16e105571364fc1db010))


## v0.16.0 (2026-05-25)

### Bug Fixes

- Make error handling up to date with API
  ([`d4f6fca`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/d4f6fca9a3a58ef9179b556f9e59401bebf5f608))

- Support for multiple statuses and task types in list_tasks
  ([`8853421`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/88534219b2e920df1922a46b9b8559f87532f9f4))


## v0.15.0 (2026-05-21)

### Bug Fixes

- Make types closer to actual API behavior
  ([`0e11753`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/0e117532571aada5362aae59ea520178653ee3cd))

### Chores

- Bump dependencies
  ([`42fc884`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/42fc884334babe901e9ebe065fa38df769c47bee))

- Remove unused rich dependency
  ([`70ebe6a`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/70ebe6ac1ebc0070275e8ce2d6d8e9c8d8347dea))

- Update AGENTS.md
  ([`a4550e8`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/a4550e8f86715f872845bb83731acf825e69f1fa))

### Features

- "fast" search depth (beta)
  ([`2e97605`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/2e9760560a931e397250356ebc327fb0bdf76800))


## v0.14.2 (2026-05-21)

### Bug Fixes

- Allow structured output schema to be a dict
  ([`87a6feb`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/87a6feb80904109787b14bec688ebcd6396b6541))

### Chores

- Upgrade semantic release action
  ([`395f7d4`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/395f7d4dd5ecdb8f73abf98c07046d61456bb8fa))


## v0.14.1 (2026-05-21)

### Bug Fixes

- Simplify linkup import with aliases
  ([`ec20202`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/ec20202014606ee5b230f2648b587495fedb5ea0))

### Chores

- Remove examples
  ([`0bccd36`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/0bccd36c6fa19511a522eacd08b334e34e67e037))

- Replace mdformat by rumdl
  ([`51d2942`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/51d29428e177b4eacc77fe486e5a00f98097aaa0))


## v0.14.0 (2026-05-20)

### Chores

- Add upper bound on supported python version
  ([`16493fa`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/16493fad04ff2ec0b3a3cc2a4bb8af982d1aaf04))

- Enable lint checks in CI
  ([`7623bc4`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/7623bc45faffb1cbdbae64dcb3b6e811c8e64a4f))

- Replace pre-commit with prek
  ([`f752423`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/f7524237c2cdff30109da43bdc82fa5ac47de823))

- Update repo tooling
  ([`7922036`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/7922036a99917fcf8ec781a3539ccf03f9a64bc8))

- Update version of uv for semantic release
  ([`5065e8d`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/5065e8dc3892cb1de8428a3f0e618894c7e18aa2))

- **uv**: Prevent install of too recent packages
  ([`ae3c055`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/ae3c055e69e5fd5f79f9af3ff1790b96da257d23))

- **uv**: Regenerate uv.lock
  ([`3afe084`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/3afe084121bd5de49189afd11d1f759b02bd8f62))

### Documentation

- Add AGENTS.md [skip release]
  ([`402b9af`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/402b9afedd7fcd319c8f421de9c04f2a03b145fc))

- Add AGENTS.md [skip release]
  ([`cffca02`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/cffca0284819a1f936a3d76aebffaa7dd6650c65))

- Add AGENTS.md [skip release]
  ([`e5c6d58`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/e5c6d582797d864adc5d1ded23b4d2921b118bbc))

### Features

- Sync research and tasks endpoints
  ([`b3f22ab`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/b3f22ab7cbaee67877bf51833e748aa18f761c06))


## v0.13.0 (2026-03-02)

### Features

- **fetch**: Add new fetch errors
  ([#63](https://github.com/LinkupPlatform/linkup-python-sdk/pull/63),
  [`d81127f`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/d81127fecae8c32d687e6d7b4f7e3a578c4ef58a))


## v0.12.0 (2026-02-16)

### Chores

- Update Python and uv versions [skip release]
  ([`2b7aef2`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/2b7aef2049fb24123ce3ff547a1d34507a19840e))

### Refactoring

- Move error handling inside request methods
  ([`33ac495`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/33ac49550f3740d0977045da394fc5aab45de482))


## v0.11.0 (2026-02-13)

### Features

- `timeout` parameter ([#61](https://github.com/LinkupPlatform/linkup-python-sdk/pull/61),
  [`9283a56`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/9283a5631d1a09c48291767df34be0980261b18b))


## v0.10.0 (2026-01-15)

### Features

- **search**: Add support for favicon
  ([`2f9632d`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/2f9632d56d750818af85a0c7d08afd057d10bfa2))


## v0.9.1 (2026-01-15)

### Bug Fixes

- Add hardcoded package version fallback
  ([`77d6e0a`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/77d6e0a61c3cb78da8dbd2c9dcf64d16c235499f))


## v0.9.0 (2025-11-14)

### Chores

- Complete test coverage
  ([`c44b3d0`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/c44b3d064a72a70b25eea9d9c4c832cce6b10431))

- Enable all lint rules
  ([`1ac1768`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/1ac17681b220c6105878f0e36dd1139695d4017a))

### Features

- Max_results parameter
  ([`be65c19`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/be65c19a02a8e69f6d984eb48e820ec19e739931))


## v0.8.0 (2025-10-31)

### Chores

- Enforce new ruff lint rules
  ([`e851c63`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/e851c63bd3df1920e55b42c0152059e54c40a266))

- Make internal modules private
  ([`b0fdff5`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/b0fdff59c5547b892b17cb0a49f4ae1a4d9f73ce))

- Use simple _ for private variables
  ([`cdcba7f`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/cdcba7f69f29b85f2d6ca7b1478754c714328563))

### Documentation

- Add pycodestyle checks
  ([`562883b`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/562883bf4ca1ba3f0029154497138d5de90192dc))

- Improve README examples readability
  ([`d00e631`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/d00e6311bcb583a5410e0157f665fe8be5be7bca))

- Mention async functions in README
  ([`f7fff79`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/f7fff790c78b6cffa73c25755d51745e699653d1))

### Features

- Accept API key as pydantic.SecretStr
  ([`1c34bf3`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/1c34bf34776e59117cf4b849c1c8445d988f7c96))


## v0.7.0 (2025-10-28)

### Features

- **fetch**: Add extract_images parameter
  ([`4204d7e`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/4204d7ea49f7ab0e1e44ac5b8f32c9964ff3935d))


## v0.6.0 (2025-09-22)

### Documentation

- Add links to the documentation
  ([`73673bb`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/73673bb1ad84e44ac98a683a1d3eedb9425244f4))

### Features

- Include_sources parameter
  ([`64fd4c5`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/64fd4c58508f447f6cbdda80e76d43a065c11df5))


## v0.5.0 (2025-09-18)

### Features

- Include_inline_citations search parameter
  ([`bd1e7fc`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/bd1e7fc0f91a832bb62813f41474e5948715249d))


## v0.4.0 (2025-09-18)

### Bug Fixes

- Specify minimal version of main requirements
  ([`9aaf6ae`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/9aaf6ae1319e47fc70b05091967d661a11820b73))

- Use API parameters order and defaults
  ([`5958298`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/595829815bfe54c3f71f75484dce56e03eb99e64))


## v0.3.0 (2025-09-17)

### Features

- Fetch endpoint
  ([`efdebdb`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/efdebdbda787542e7b38e5058e455c7d694db5df))


## v0.2.11 (2025-09-17)

### Bug Fixes

- From_ and to_date default values
  ([`575e7c4`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/575e7c43bd6b255853139da1e81ebfaca6285ce4))

### Chores

- Add load_dotenv in example scripts
  ([`e6babc9`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/e6babc998422d4544f7e53373435aa5bcb44f5f0))

- Pass all parameters in search payload
  ([`2319388`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/23193883dba53b049f565f1ca772c9e508aa6746))

### Refactoring

- Streamline tests and add more
  ([`2d58d85`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/2d58d85881b74098a51cad27b93dbb4228cfc441))


## v0.2.10 (2025-09-16)

### Bug Fixes

- Small docstring wording
  ([`6330633`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/63306336551a5f381f0c2a6fa726f87046eafe1a))

- Types and documentation improvements
  ([`ecdb6a9`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/ecdb6a9639c8be58fea454c42dab9312dc015fe5))

### Chores

- Format and lint
  ([`a4d10d7`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/a4d10d739f24d12190b7e5ba6954aaa252507a5d))

- Standardize tools and configs
  ([`8c9224d`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/8c9224da3409884126f6d44135f8b4976f4b741e))

- Update PR template
  ([`8567d24`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/8567d247dbb9a5987bfc036fe8358b76d3dfa22f))

- Use lowest supported Python version
  ([`fe3a7fe`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/fe3a7fed6c5c6f5fd1bc164774ff4dc65f5f5b5e))

- Use rich.print in examples
  ([`94d5d42`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/94d5d4211f852214a7c3f67d69875f9cb057ff26))


## v0.2.9 (2025-09-15)

### Bug Fixes

- Fetch all commit history for semantic-release
  ([`d811306`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/d81130693ae04d6b2c13908811adeb0783a8ae65))

- Install uv in python-semantic-release action
  ([`b7af0eb`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/b7af0eb341ab091408d5b8aace0f630a80683006))

- Keep version in 0.x.x
  ([`0bbcfbd`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/0bbcfbdce4e9f4833812a8d39c77f7b23d05ac51))

- Outdated package version
  ([`20ae5d0`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/20ae5d0201614c908d6e2f152637b3760059ea8c))

- Update and simplify github actions
  ([`8e48be3`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/8e48be3b29d47fe9363f5e03f83ffc99671af8a7))

- Use semantic release GH actions
  ([`069f7e0`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/069f7e039ba3e4723111ba88aae9ecaa3e4eaa75))

### Chores

- Add semantic release ([#34](https://github.com/LinkupPlatform/linkup-python-sdk/pull/34),
  [`a666011`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/a6660113c41e72af918c134e2f2ba304c874a169))

- Add uv for python sdk ([#33](https://github.com/LinkupPlatform/linkup-python-sdk/pull/33),
  [`2fb5984`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/2fb5984af59244f314840e4a5f0888c1921cea2c))

- Don't parse squash commits in semantic release
  ([`586321c`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/586321c8f79eeb08793753e5aac87f4e754ab1b0))

- Revert version to pre-semantic-release
  ([`89acb72`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/89acb729c97230179bab715eac6a4a7cc975652d))

- Specify environment in release job
  ([`223b02d`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/223b02de596c711d1fe9fed96cb239f47fc255fc))

- Update pyproject.toml config
  ([`c573df7`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/c573df7f600c5f8d28346ded7043047fc65d656c))

### Continuous Integration

- Automatically bump pyproject.toml version
  ([`ee13a6a`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/ee13a6a36f5fbbb508d1a880ed2c377b8ad38a81))

- Change secret variable name
  ([`7e750d1`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/7e750d11a6d34d4971ba16190b5cef02fadd498c))

- Expose outputs in release job
  ([`0af76cb`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/0af76cb83614e88f796ca45ca614ba1d111e3c0e))

- Skip remaining release jobs if no release is made
  ([`16df390`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/16df390ed42e39e5ba8b4c96bda376baa6cf5fad))


## v0.2.8 (2025-07-01)

### Bug Fixes

- Send search params as json instead of form-encoded
  ([#32](https://github.com/LinkupPlatform/linkup-python-sdk/pull/32),
  [`c1d1f9f`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/c1d1f9fb5b384c43db03f783dfc4fe146d314844))


## v0.2.7 (2025-06-23)


## v0.2.6 (2025-05-30)

### Documentation

- Fix URL in README
  ([`706e59b`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/706e59bb47e375bc435ed29a036b173f11a51925))


## v0.2.5 (2025-05-09)

### Bug Fixes

- From_date/to_date in async search
  ([`e35c84b`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/e35c84bc2298a1450da3580068b385670dc14ab1))

### Chores

- Bump version
  ([`10f3bcf`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/10f3bcff79f8a411ffa90024f192c98037d24c05))


## v0.2.4 (2025-03-19)


## v0.2.3 (2025-02-06)

### Features

- Implement new api errors and use the post endpoint
  ([`672bcea`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/672bceae398a8736417535be2b38c838ca7bd6bd))

- Upgrade version
  ([`40391df`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/40391df9c4414f2264f0fc3f1d9ceb888b60141f))


## v0.2.2 (2025-01-09)

### Bug Fixes

- Bad wording for the world Authentication
  ([`8ec5f19`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/8ec5f1990b0b24dbf3bed0d2d95f44d406594bc0))


## v0.2.1 (2024-12-10)


## v0.2.0 (2024-12-03)

### Bug Fixes

- Don't handle missing structured schema error
  ([`2f41452`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/2f414525135b6a7a002e5913ecd8ba9ec5544540))

- SDK version in client
  ([`687730a`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/687730ae6c849818f19221cd4df01524cbc52dd8))

### Chores

- Add gitleaks in pre-commit and update hook versions
  ([`916e461`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/916e4614e8bbb929b1b14505cbfacac78b7d0964))

- Drop support for Python 3.8 and test in Python 3.13
  ([`5343cbd`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/5343cbd15f60d5da2df2860b7049e4894cbda2b4))

- Read the package version from linkup/_version.py
  ([`b52ac83`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/b52ac8341b14148fbead49d33671a6487abd05cd))

- Remove content entrypoint
  ([`f52b0e6`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/f52b0e6d4167ea2cefb1edee1ef8bab068fb25ab))

- Update package version to 0.2.0
  ([`dcb7586`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/dcb7586a57a003fa0db1309ab212481791fc52f9))

### Documentation

- Add Client docstring
  ([`58abc7c`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/58abc7c8ebefbff2d123e7b966dbf23baee4f895))

- Add PR template
  ([`9860498`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/9860498b820b67bae54fc8c1b7c05c87906c6fd0))

- Move example README section in usage
  ([`d2f4c0f`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/d2f4c0fb13e6c02e381cf81c90d643e4430d5cae))


## v0.1.8 (2024-11-21)

### Bug Fixes

- Remove some default values, improve docstrings and error types
  ([`dbcb31a`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/dbcb31abea725763d9633f7decc4677281175621))

### Chores

- Upgrade package to version 0.1.8
  ([`ae15b5f`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/ae15b5fdf66e1ff3e79fb173ac97d8629f5da207))

### Continuous Integration

- Only test min/max python versions
  ([`f04a578`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/f04a5789627a6f54109d8beb444efc86724c355b))

### Documentation

- Update documentation
  ([`b661d1a`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/b661d1a290957e10b9291e8ad75f6aa6678f15cf))

### Testing

- Improve test setup
  ([`d2bb998`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/d2bb9981425484cf88057a78c59256158d205c4e))


## v0.1.7 (2024-11-20)

### Bug Fixes

- Add missing setuptools dev dependency
  ([`bda6803`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/bda6803ee9c3852857d9bb9c66d3af42646b5979))

- Add py.typed marker
  ([`42d1e7d`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/42d1e7dbce92d3fff5dc7752088c82ef82492a53))

### Chores

- Remove requirements.txt
  ([`ca8510e`](https://github.com/LinkupPlatform/linkup-python-sdk/commit/ca8510ec566981884468b96657d720e178a857d8))


## v0.1.6 (2024-11-20)


## v0.1.5 (2024-11-15)


## v0.1.4 (2024-11-15)


## v0.1.3 (2024-11-15)


## v0.1.2 (2024-11-14)

- Initial Release
