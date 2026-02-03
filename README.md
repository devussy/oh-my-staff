# MSS Staff - Work Automation Tools

업무 지원 도구 모음: JIRA, Confluence, Slack, Google Workspace 통합 자동화

## 개요

이 프로젝트는 MCP (Model Context Protocol) 서버를 기반으로 다음 업무를 자동화합니다:

1. **Weekly Report 생성** - 여러 데이터 소스 통합
2. **Slack 메시지 분석** - 토론 요약, 액션 아이템 추출
3. **JIRA 운영 개선안** - 벨로시티 분석, 사이클 타임
4. **Confluence 맥락 파악** - 도메인 지식 추출
5. **회사 도메인 지식 분석** - 지식 베이스 분석

## 아키텍처

5개의 독립적인 MCP 서버:

- **JIRA Server** - 이슈 관리 및 분석
- **Confluence Server** - 문서 검색 및 지식 추출
- **Slack Server** - 메시지 분석 및 요약
- **Google Workspace Server** - Docs/Sheets 읽기
- **Report Server** - 통합 리포트 생성

## 설치

### 1. 환경 설정

```bash
# 가상 환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. API 토큰 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일을 편집하여 실제 API 토큰 입력
```

#### API 토큰 발급 방법:

**JIRA & Confluence:**
1. https://id.atlassian.com/manage-profile/security/api-tokens
2. "Create API token" 클릭
3. 생성된 토큰을 .env에 복사

**Slack:**
1. https://api.slack.com/apps
2. 앱 생성 또는 선택
3. OAuth & Permissions에서 Bot Token 복사
4. 필요한 스코프: `channels:history`, `channels:read`, `users:read`, `search:read`

**Google Workspace:**
1. https://console.cloud.google.com/
2. API 및 서비스 > 사용자 인증 정보
3. OAuth 2.0 클라이언트 ID 생성
4. credentials.json 다운로드
5. 첫 실행 시 브라우저에서 인증 (token.json 자동 생성)

### 3. 연결 테스트

```bash
# API 연결 확인
python scripts/test_connections.py
```

## MCP 서버 설정

`.mcp.json` 파일이 프로젝트 루트에 자동으로 생성됩니다.

Claude Code에서 자동으로 인식합니다.

## 사용 방법

### Claude Code에서 사용

```
# 주간 보고서 생성
"지난 주 주간 보고서 생성해줘"

# JIRA 이슈 검색
"최근 완료된 이슈 10개 조회해줘"

# Confluence 페이지 검색
"API 관련 문서 찾아줘"

# Slack 메시지 분석
"지난 주 dev-team 채널 토론 요약해줘"

# 통합 분석
"프로젝트 건강도 체크해줘"
```

### 직접 호출 (개발/테스트용)

```python
# 예제는 tests/ 디렉토리 참고
```

## MCP 도구 목록

### JIRA Server (6개 도구)
- `jira_search_issues` - JQL 쿼리로 이슈 검색
- `jira_get_issue` - 특정 이슈 상세 조회
- `jira_get_sprint` - 스프린트 정보 조회
- `jira_analyze_velocity` - 벨로시티 분석
- `jira_analyze_cycle_time` - 사이클 타임 분석
- `jira_suggest_improvements` - 운영 개선안 제시

### Confluence Server (6개 도구)
- `confluence_search_pages` - CQL로 페이지 검색
- `confluence_get_page` - 특정 페이지 조회
- `confluence_get_space` - 스페이스 정보 조회
- `confluence_get_recent_updates` - 최근 업데이트 조회
- `confluence_extract_context` - 맥락 정보 추출
- `confluence_analyze_knowledge_base` - 지식 베이스 분석

### Slack Server (6개 도구)
- `slack_search_messages` - 메시지 검색
- `slack_get_channel_history` - 채널 히스토리 조회
- `slack_get_thread` - 스레드 대화 조회
- `slack_get_user_info` - 사용자 정보 조회
- `slack_analyze_sentiment` - 감정 분석
- `slack_summarize_discussions` - 토론 요약

### Google Workspace Server (4개 도구)
- `google_read_doc` - Google Docs 읽기
- `google_read_sheet` - Google Sheets 읽기
- `google_list_docs` - Docs 목록 조회
- `google_extract_data` - 구조화된 데이터 추출

### Report Server (5개 도구)
- `report_generate_weekly` - 주간 보고서 생성
- `report_analyze_jira_operations` - JIRA 운영 분석
- `report_summarize_slack` - Slack 활동 요약
- `report_extract_domain_knowledge` - 도메인 지식 추출
- `report_export_markdown` - 마크다운 내보내기

## 프로젝트 구조

```
mss-staff/
├── servers/              # MCP 서버 구현
│   ├── common/          # 공통 유틸리티
│   ├── jira_server/
│   ├── confluence_server/
│   ├── slack_server/
│   ├── google_workspace_server/
│   └── report_server/
├── config/              # 설정 파일
├── data/                # 데이터 및 캐시
├── reports/             # 생성된 리포트
├── scripts/             # 헬퍼 스크립트
└── tests/               # 테스트
```

## 개발 로드맵

### Phase 1: MVP (현재)
- [x] 프로젝트 초기 설정
- [ ] 공통 유틸리티 구현
- [ ] 5개 MCP 서버 기본 구현
- [ ] Claude Code 통합
- [ ] 주간 보고서 생성

### Phase 2: 확장 기능
- [ ] 고급 분석 기능 (벨로시티, 사이클 타임)
- [ ] 맥락 추출 및 도메인 지식 분석
- [ ] 다양한 리포트 템플릿
- [ ] 히스토리 관리 및 트렌드 분석

### Phase 3: Agent & Skill
- [ ] 5개 Agent 구현 (회고, 건강도 체크, 온보딩, 리스크 분석, 커뮤니케이션)
- [ ] 7개 Skill 구현 (빠른 조회 및 리포트 생성)

### Phase 4: 최적화
- [ ] 성능 개선 및 캐싱 전략
- [ ] 에러 복구 전략
- [ ] 대시보드 및 알림 시스템

## 보안

- API 토큰은 환경 변수로만 관리
- `.env` 파일은 절대 커밋하지 않음
- 로그에서 민감 정보 자동 마스킹
- 토큰 권한 최소화 (읽기 전용)

## 트러블슈팅

### API 연결 실패
```bash
# 연결 테스트 스크립트 실행
python scripts/test_connections.py

# 로그 확인
tail -f mss-staff.log
```

### MCP 서버 인식 안 됨
1. `.mcp.json` 파일 확인
2. Claude Code 재시작
3. 환경 변수 설정 확인

### 캐시 문제
```bash
# 캐시 초기화
rm -rf data/cache/*
```

## 라이선스

MIT License

## 기여

Issue 및 Pull Request 환영합니다.
