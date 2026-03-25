# mh-config-manager (`config_manager`)

YAML·Python 설정 파일을 **한 번에 로드**하고, **다른 파일·값·함수를 참조하는 표현**을 설정 트리 안에서 풀어 주는 Python 라이브러리입니다.  
설정을 “평범한 dict”로 만든 뒤, 핸들러 파이프라인으로 단계적으로 가공합니다.

---

## 왜 필요한가 (문제 / 필요성)

- 설정을 여러 파일로 나누거나, 공통 베이스 위에 덮어쓰고 싶을 때가 많습니다.
- 단순히 JSON/YAML만 읽으면 **파일 간 참조·상호 참조·재사용**을 매번 직접 코드로 풀어야 합니다.
- 이 라이브러리는 **로드(Accessor)** 와 **의미 확장(Handler)** 을 분리해, 설정 포맷과 “설정이 의미하는 동작”을 조합할 수 있게 합니다.

---

## 핵심 아이디어 (의의)

| 구성요소 | 역할 |
|----------|------|
| **ConfigAccessor** | 파일 경로 → `dict` 로 읽기(및 필요 시 쓰기). 포맷별 구현(YAML, Python 실행 등). |
| **Handler** | 이미 로드된 `dict`를 받아 변환한 뒤 다음 핸들러로 넘김. **파이프라인**입니다. |
| **ConfigLoader** | `load_config`(파일만) / `load_full_config`(파일 또는 dict + 전체 핸들러 적용). |
| **RecursiveContext** | dict·list·tuple을 재귀적으로 순회하며 값을 치환·필터링. |
| **DictTool** | dict 병합, 경로(`a.b.c`)로 get/set, 임시 키 필터 등. |
| **Factory** | 기본 Accessor·Handler·Loader 조합을 한 번에 만들어 줌. |

즉, **“설정 파일 = 데이터 + 선언적 참조 규칙”** 을 코드 한두 줄로 끝내고 싶을 때 쓰기 좋습니다.

---

## 설치

```bash
pip install mh-config-manager
```

개발(소스에서 editable):

```bash
pip install -e ".[dev]"
```

**패키지 이름**은 PyPI에서 `mh-config-manager`이고, **import 이름**은 `config_manager`입니다.

---

## 빠른 시작 (`Factory` 사용)

프로젝트에서 권장되는 진입점은 `Factory`입니다. 내부에서 `ConfigLoader`와 핸들러 목록을 맞춰 줍니다.

```python
from pathlib import Path
from config_manager import Factory

factory = Factory()
loader = factory.make_config_loader()

config = loader.load_full_config(path=Path("config.yaml"))
# 또는 이미 dict가 있으면:
# config = loader.load_full_config(config={"key": "value"})
```

테스트 코드(`tests/config_manager_test.py`)처럼 **Python 설정 파일**을 쓰려면 `Factory`가 기본으로 쓰는 `PythonConfigAccessor`와 맞아야 합니다.

---

## 설정 포맷 (Accessor)

| 클래스 | 설명 |
|--------|------|
| **YamlConfigAccessor** | YAML 파일 로드/저장 (`yaml` 필요). |
| **PythonConfigAccessor** | `runpy.run_path`로 `.py`를 실행하고, `__`로 시작하지 않는 전역 변수를 dict로 수집. |

`PythonConfigAccessor.dump_config`는 `mmengine.config.Config`를 사용합니다. 해당 기능을 쓰면 `mmengine` 설치가 필요합니다.

---

## 핸들러(기능) 개요

핸들러는 `ConfigLoader.load_full_config` 안에서 **등록된 순서대로** `handle(config)`가 호출됩니다.  
`Factory.make_config_handlers`의 순서가 곧 동작 순서입니다(중복 등록된 핸들러가 있으면 그만큼 두 번 실행됩니다).

| 핸들러 | 하는 일 (요약) |
|--------|----------------|
| **FileConfig_ReferHandler** | 문자열이 `@file_cfg:` 로 시작하면 해당 경로의 설정을 다시 `load_full_config`로 불러와 치환. |
| **Tuple_Merge_Handler** | “dict만 담긴 tuple”이면 `DictTool.merge`로 하나의 dict로 병합. |
| **Base_Flat_Handler** | 최상위 `_base` 키가 있으면 베이스 dict와 현재 dict를 `DictTool.merge_config`로 합침. |
| **Function_Handler** | 문자열이 `@func:` 로 시작하면 `eval`로 실행해 값으로 치환. **신뢰할 수 있는 설정에만 사용**하세요. |
| **Val_ReferHandler** | `@val:` + 경로(예: `a.b`) 형태면 현재 config 트리에서 `DictTool.get`으로 값을 가져와 치환. |
| **Temp_Value_Filter_Handler** | **키**가 `_`로 시작하는 항목을 트리에서 제거(임시 값). |

`handler/db_handler.py`에 DB 연동 핸들러 스켈레톤이 주석으로만 있습니다.

---

## 참조 예시

아래는 **문자열 마커**와 **구조**를 쓰는 방식입니다. 실제로는 `Factory`의 핸들러 순서(파일 참조 → 튜플 병합 → `_base` → …)에 따라 중간 결과가 달라질 수 있으니, 겹치게 쓸 때는 한 번에 하나씩 검증하는 것을 권장합니다.

### 파일 참조 (`@file_cfg:`)

값이 **문자열**이고 `@file_cfg:` 로 시작하면, 접두어를 뗀 경로를 `ConfigLoader.load_full_config`로 다시 읽어 그 자리에 **치환**합니다. YAML·Python 등은 현재 `ConfigLoader`에 연결된 `ConfigAccessor`가 읽을 수 있는 경로면 됩니다.

**YAML 예시** (`main.yaml`)

```yaml
# 같은 디렉터리의 defaults.yaml 전체를 불러와 이 키 값으로 씀
defaults: "@file_cfg:./defaults.yaml"

nested:
  extra: "@file_cfg:./extra.yaml"
```

**Python 설정 예시** (문자열로 경로를 만들 때)

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent

other = f"@file_cfg:{HERE / 'piece.yaml'}"
```

### 값 참조 (`@val:`)

값이 `"@val:..."` 형태면, **첫 번째 `:` 뒤**를 점(`.`)으로 나눈 경로로 현재 설정 트리에서 값을 찾아 치환합니다. (`Val_ReferHandler` → `DictTool.get`)

```yaml
seed: 42
training:
  # seed 키의 값(42)을 그대로 가져옴
  same_seed: "@val:seed"

nested:
  value: 100

flat:
  # nested.value → 100
  copy: "@val:nested.value"
```

주의: `@val:` 뒤에는 **한 번만** `:` 로 나누므로, 경로에 `:` 가 들어가는 표현은 피하세요.

### 베이스 참조 (`_base`)

최상위에 **`_base` 키**가 있으면, 그 값(dict)을 베이스로 두고 **나머지 키**를 `DictTool.merge_config`로 덮어씁니다. 처리 후 `_base` 키는 제거됩니다.

```yaml
_base:
  lr: 0.01
  epochs: 100

# 아래는 베이스 위에 덮어쓰기
lr: 0.001
batch_size: 32
```

결과에는 `lr`, `epochs`, `batch_size`가 남고, `lr`는 `0.001`로 덮입니다.

`_base` 자리에 **dict만 담긴 튜플**을 두고 싶다면, 먼저 **파일 참조·튜플 병합** 핸들러가 튜플을 dict로 정리한 뒤 `Base_Flat_Handler`가 동작하도록 구성할 수 있습니다(테스트의 `tests/a.py` 패턴).

### 튜플 병합 (dict 튜플)

**dict만** 담긴 `tuple`이면 여러 조각 dict를 순서대로 합칩니다.

```python
merged = (
    {"a": 1, "shared": 10},
    {"b": 2, "shared": 20},
)
# 핸들러 적용 후 하나의 dict로 병합 (같은 키는 뒤쪽이 유리 — DictTool.merge 규칙 따름)
```

### 함수 참조 (`@func:`)

문자열이 `@func:` 로 시작하면 접두어 뒤를 **현재 config를 locals로** `eval`합니다. **신뢰할 수 있는 설정에만** 사용하세요.

```yaml
two: "@func:1 + 1"
ref_other: "@func:config['lr'] * 2"
```

(`ref_other` 예는 `Function_Handler`가 돌 때점의 config 트리에 `lr` 등이 이미 있어야 합니다.)

---

## 참조·표현 요약

| 종류 | 형태 | 비고 |
|------|------|------|
| 파일 | `@file_cfg:<경로>` | 경로는 `load_full_config`에 넘길 수 있는 문자열 |
| 값 | `@val:<a.b.c>` | 현재 dict에서 점 경로로 조회 |
| 베이스 | 최상위 `_base` | dict 병합 후 `_base` 제거 |
| 튜플 병합 | `(dict, dict, …)` | dict만 들어 있는 튜플 |
| 함수 | `@func:<표현식>` | `eval` — 보안 주의 |

실제 동작은 핸들러 순서와 데이터 형태에 따라 달라지므로, 복잡한 설정은 테스트로 순서를 확인하는 것이 좋습니다.

---

## 의존성 참고

`pyproject.toml`의 `dependencies`는 비어 있을 수 있으나, 코드에서 선택적으로 사용합니다.

- **YAML**: `YamlConfigAccessor` → `pyyaml` 등
- **Python dump**: `PythonConfigAccessor.dump_config` → `mmengine`
- **테스트**: `pytest` (개발 extra)

사용하는 Accessor/기능에 맞춰 직접 설치하세요.

---

## 보안 주의

- **Function_Handler**는 `eval`을 사용합니다. 신뢰할 수 없는 설정 파일에는 사용하지 마세요.

---

## 라이선스

MIT — 저장소의 `LICENSE` 파일을 참고하세요.

---

## 개발

```bash
pip install -e ".[dev]"
python -m pytest
```

빌드·PyPI 배포 스크립트(`build.cmd`, `deploy.cmd` 등)는 프로젝트 루트에 있습니다.
