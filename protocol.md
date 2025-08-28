# Gemini Protocol Log

이 파일은 Gemini 에이전트와 프로젝트 소유자가 프로젝트의 주요 변경 사항을 추적하기 위해 사용하는 로그입니다.
This file is a log used by the Gemini agent and the project owner to track significant changes in the project.

---

## 2025-08-28

**아티클 페이지 이미지 갤러리 개선 (Article Page Image Gallery Improvement)**

*   **기능 (Feature):** `article.html`의 이미지 갤러리 기능을 개선했습니다.
*   **변경 (Change):** 기존의 직접 구현된 이미지 뷰어를 `Swiper.js` 라이브러리 기반의 캐러셀(carousel)로 교체했습니다.
*   **세부사항 (Details):**
    *   CDN을 통해 Swiper.js 라이브러리 및 관련 CSS를 추가했습니다.
    *   `article.html`의 HTML 구조를 Swiper.js에 맞게 재구성했습니다.
    *   관련 아티클 폴더 내의 모든 `.webp` 이미지들을 동적으로 찾아 갤러리에 포함시켰습니다.
    *   기존의 충돌 가능성이 있는 CSS 스타일과 불필요해진 `js/main.js` 파일을 제거하여 코드를 정리했습니다.
*   **이유 (Reason):** 사용자의 요청에 따라 모바일 환경에 친화적인 최신 이미지 스와이프 경험을 제공하기 위함입니다.

---

## 2025-08-27

**프로토콜 초기화 및 주요 작업 요약 (Protocol Initialized & Summary of Major Tasks)**

*   **데이터 관리 시스템 도입 (Data Management System Introduced):**
    *   기존의 하드코딩 방식에서 벗어나, 각 제품 폴더 내에 `info.txt` 파일을 두어 `era`, `status` 등의 메타데이터를 관리하는 시스템을 도입함.
    *   `build.py` 스크립트는 이제 `info.txt` 파일을 자동으로 읽으며, 파일이 없을 경우 기본 템플릿을 생성함.

*   **빌드 스크립트 고도화 (Build Script Advanced):**
    *   `build.py`에 통계(총 제품 수, 마지막 빌드 시간, 전체 용량)를 계산하는 기능을 추가함.
    *   계산된 통계는 메인 `index.html` 페이지 상단에 표시됨.

*   **개발 워크플로우 자동화 (Development Workflow Automated):**
    *   `start_preview.command` 스크립트를 생성함.
    *   이 스크립트는 사이트 빌드 (`build.py` 실행)와 로컬 서버 실행을 한 번의 더블클릭으로 자동화하여, `git push` 없이 로컬 환경에서 쉽게 변경사항을 확인할 수 있도록 함.
