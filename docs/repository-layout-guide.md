# Hướng dẫn cấu trúc repository `skill-sa`

Tài liệu này giải thích layout hiện tại của repository, tác dụng của từng nhóm file và cách Claude sử dụng chúng khi một SA skill chạy.

## 1. Bản đồ tổng thể

```text
skill-sa/
├── .claude-plugin/                 # Metadata để Claude cài và discover plugin
│   ├── plugin.json
│   └── marketplace.json
├── docs/                           # Tài liệu dành cho người đọc
│   ├── sa-learning-guide.md
│   └── repository-layout-guide.md
├── examples/                       # Ví dụ hoàn chỉnh để học và kiểm tra tính nhất quán
│   ├── README.md
│   └── express-lane/
│       ├── sa-config.yaml
│       ├── architecture-brief.md
│       ├── decisions/
│       ├── hld/
│       ├── flows/
│       ├── interfaces/
│       ├── data/
│       └── reviews/
├── scripts/                        # Kiểm tra cơ học cho plugin và example
│   └── validate_repo.py
├── skills/                         # Các skill Claude có thể discover
│   ├── architect/SKILL.md
│   ├── adr/SKILL.md
│   ├── hld/SKILL.md
│   ├── flow/SKILL.md
│   ├── interface/SKILL.md
│   ├── data/SKILL.md
│   ├── review/SKILL.md
│   └── method/
│       ├── SKILL.md
│       ├── standards/
│       └── templates/
├── README.md                       # Hướng dẫn sử dụng nhanh
├── LICENSE                         # Giấy phép MIT
└── .gitignore                      # File không đưa vào Git
```

Repository được chia thành năm lớp:

1. **Packaging:** `.claude-plugin/`
2. **Agent instructions:** `skills/*/SKILL.md`
3. **Quality rules và output skeletons:** `skills/method/standards/`, `templates/`
4. **Learning và examples:** `docs/`, `examples/`
5. **Deterministic validation:** `scripts/`

---

## 2. Claude nạp các file theo thứ tự nào?

Claude không nên đọc toàn bộ repository mỗi lần chạy một skill.

```text
1. Skill metadata
   ↓
2. SKILL.md của skill được trigger
   ↓
3. method/SKILL.md + lightweight workflow
   ↓
4. Một standard và template đúng với artifact
   ↓
5. Evidence và artifact liên quan trong project của người dùng
```

Ví dụ khi chạy `/sa:adr`:

```text
skills/adr/SKILL.md
  → skills/method/SKILL.md
  → standards/workflow.md
  → standards/adr.md
  → templates/adr.md
  → architecture brief, existing ADRs và source evidence của project
```

Ví dụ khi chạy `/sa:hld` container view:

```text
skills/hld/SKILL.md
  → skills/method/SKILL.md
  → standards/workflow.md
  → standards/hld.md
  → standards/diagrams.md
  → templates/hld-catalogue.md khi cần
  → architecture brief, ADRs và existing diagrams của project
```

Nguyên tắc này gọi là progressive disclosure: chỉ nạp detail khi task thật sự cần.

---

## 3. Các file ở repository root

### `README.md`

Đối tượng đọc: người mới cài hoặc muốn dùng plugin nhanh.

Tác dụng:

- Giải thích plugin làm gì.
- Hướng dẫn cài đặt.
- Giới thiệu `/sa:architect` là entry point.
- Liệt kê bảy user-facing skills.
- Giải thích ba mode `quick`, `brief`, `artifact`.
- Cho ví dụ prompt.

README không phải instruction chi tiết cho Claude và không nên chứa toàn bộ phương pháp SA.

### `LICENSE`

Giấy phép MIT cho repository. Nó xác định quyền sử dụng, sửa đổi và phân phối source.

### `.gitignore`

Khai báo các file cục bộ không nên commit, ví dụ cache hoặc generated files nếu có.

---

## 4. `.claude-plugin/` — lớp packaging

### `.claude-plugin/plugin.json`

Manifest chính của plugin.

Chứa:

- Plugin name: `sa`.
- Version.
- Description.
- Author, homepage và repository.
- License.
- Search keywords.

Tác dụng:

- Claude biết đây là plugin nào.
- Xác định namespace `sa:`.
- Marketplace và CLI có thể hiển thị metadata đúng.

File này không quyết định cách một SA task được thực hiện.

### `.claude-plugin/marketplace.json`

Manifest cho marketplace source.

Chứa:

- Tên marketplace package.
- Owner.
- Plugin source.
- Category và description.

Tác dụng: cho phép lệnh cài đặt marketplace tìm và cài plugin.

---

## 5. `skills/` — lớp hành vi của Claude

Mỗi thư mục skill có một `SKILL.md` cùng tên.

```text
skills/<skill-name>/SKILL.md
```

Một `SKILL.md` gồm:

1. **Frontmatter:** tên, description và tool permissions.
2. **Body:** inputs, method, output, boundary và references.

Frontmatter `description` quyết định skill có trigger hay không. Body chỉ được đọc sau khi skill đã được chọn.

## 5.1. `skills/architect/SKILL.md`

Vai trò: entry point chính.

Dùng khi người dùng chưa biết cần artifact nào hoặc muốn:

- Hiểu problem.
- Phân tích repository.
- So sánh options.
- Đề xuất target architecture.
- Tạo architecture brief.
- Route sang skill chuyên biệt.

Input chính:

- User request.
- Requirements.
- Repository evidence.
- Existing architecture artifacts.
- Constraints và metrics.

Output:

- `quick`: conversation answer.
- `brief`: `architecture-brief.md`.
- `artifact`: chuyển sang ADR/HLD/flow/interface/data/review.

Đây là file được ưu tiên dùng cho hầu hết yêu cầu SA.

## 5.2. `skills/adr/SKILL.md`

Vai trò: ghi lại một quyết định kiến trúc quan trọng.

Input:

- Architecture brief hoặc requirements.
- Drivers và constraints.
- Existing ADRs.
- Affected design.

Output mặc định:

```text
docs/architecture/decisions/ADR-NNNN-<slug>.md
```

Không dùng cho implementation detail có thể đảo ngược dễ dàng.

## 5.3. `skills/hld/SKILL.md`

Vai trò: mô hình hóa static structure.

Input:

- Architecture brief.
- Accepted ADRs.
- Existing diagrams.

Output:

- System context view.
- Container view.
- Component view khi cần.
- Deployment view khi placement/failure domain quan trọng.
- Catalogue bổ sung nếu diagram quá nhiều detail.

Không dùng để quyết định sync hay async; quyết định phải có trước hoặc được xử lý bởi `architect`/`adr`.

## 5.4. `skills/flow/SKILL.md`

Vai trò: mô hình hóa runtime behaviour.

Input:

- Architecture brief.
- HLD.
- ADRs.
- Existing contracts.

Output:

```text
docs/architecture/flows/<flow-name>.puml
```

Có thể có narrative `.md` nếu timeout, retry, consistency và recovery không thể trình bày rõ trong diagram.

## 5.5. `skills/interface/SKILL.md`

Vai trò: thiết kế boundary contract.

Input:

- Named consumers và outcome.
- Architecture brief.
- Runtime flows.
- Data vocabulary.
- Existing specs.

Output:

- OpenAPI cho synchronous API.
- AsyncAPI cho event contract.

Không implementation handler hoặc client code.

## 5.6. `skills/data/SKILL.md`

Vai trò: data architecture qua component/team boundary.

Input:

- Architecture brief.
- HLD và flows.
- Contracts.
- Existing data documentation.
- Regulatory requirements.

Output:

- `data-design.md`.
- `migration-plan.md` khi existing data phải thay đổi hoặc di chuyển.

Không xử lý SQL, index tuning hoặc query optimisation trừ khi chúng ảnh hưởng architecture driver.

## 5.7. `skills/review/SKILL.md`

Vai trò: independent architecture review.

Input:

- Architecture brief.
- Relevant ADRs, HLD, flows, contracts và data design.
- Drivers và repository evidence.

Output:

- Findings trong conversation; hoặc
- `design-review-<date>.md`.

Review không sửa design. `context: fork` giúp reviewer có fresh context, còn `disallowed-tools` hạn chế edit.

## 5.8. `skills/method/SKILL.md`

Vai trò: shared contract nội bộ.

Chứa:

- Danh sách core skills.
- Ba mode.
- Minimal workflow.
- Shared quality rules.
- Optional config.
- Bảng route từ task sang standard/template.

Tác dụng: tránh lặp cùng một instruction trong bảy user-facing skill.

---

## 6. `skills/method/standards/` — quality rules

Standard trả lời câu hỏi:

> Artifact này cần đạt điều kiện gì để được xem là tốt?

### `core-flow.md`

Định nghĩa core flow và điều kiện để promote từ architecture brief sang artifact chuyên biệt.

### `workflow.md`

Workflow dùng chung:

1. Understand.
2. Scope.
3. Produce.
4. Check and report.

Quy định khi nào cần hỏi, khi nào được dùng assumption và khi nào cần confirmation.

### `adr.md`

Quality bar cho ADR:

- Một decision.
- Ít nhất hai credible options.
- Consequences.
- Reversibility.
- Compliance.

### `hld.md`

Quality bar cho HLD:

- Scope/audience.
- Responsibility và owner.
- Labelled relationships.
- Trust boundaries.
- Coupling checks.
- Consistency với ADR.

### `runtime-flow.md`

Quality bar cho runtime flow:

- Trigger và terminal states.
- Happy/failure paths.
- Timeout/retry.
- Idempotency.
- Durability/consistency.
- Recovery và detection signals.

### `interface.md`

Quality bar cho contract:

- Named consumer.
- Auth/error/limits.
- Idempotency hoặc deduplication.
- Examples.
- Compatibility.
- Migration và sunset cho breaking change.

### `data.md`

Quality bar cho data architecture:

- Một authoritative owner.
- Classification.
- Retention/deletion.
- Consistency mechanism.
- Migration/coexistence.

### `review.md`

Định nghĩa:

- Mười review dimensions.
- Finding severity.
- Verdict calculation.
- Evidence requirement.

### `diagrams.md`

Quy tắc cho:

- C4 levels.
- PlantUML.
- Element/relationship naming.
- Sync/async visual distinction.
- Sequence và data diagrams.

### `quality-bar.md`

Quality rules chung áp dụng cho mọi output:

- Scope rõ.
- Evidence và assumptions.
- Measurable drivers.
- Real alternatives.
- Negative consequences.
- Consistent names/ownership.
- Cross-cutting concerns.

### `tailoring.md`

Chọn output proportional:

- `quick`.
- `brief`.
- `artifact`.
- `artifact + review`.

### `deployment-view.md`

Detail chỉ dùng khi thiết kế deployment:

- Environment.
- Node placement.
- Region/AZ.
- Scaling.
- Network paths.
- Failure domains.
- Shared infrastructure.

### `operating-guardrails.md`

Behavioral boundaries:

- Không sửa source code trong SA documentation task.
- Không invent evidence.
- Giữ writes visible.
- Minimise context.
- Review độc lập.

## 7. `skills/method/templates/` — output skeletons

Template trả lời:

> Khi cần tạo artifact, cấu trúc mặc định của file là gì?

### `architecture-brief.md`

Artifact trung tâm, gom:

- Problem/outcome.
- Scope.
- Drivers.
- Current-state impact.
- Options/recommendation.
- Proposed architecture.
- Interfaces/data.
- Cross-cutting concerns.
- Decisions/risks/open questions.
- Next steps.

### `adr.md`

Skeleton cho một architecture decision record.

### `hld-catalogue.md`

Bảng bổ sung cho diagram:

- Elements.
- Relationships.
- Structural checks.

### `deployment-catalogue.md`

Bảng node, placement, scaling, network path và failure domain cho deployment view.

### `flow-narrative.md`

Runtime detail khi diagram không đủ chỗ:

- Steps.
- Timeout/retry.
- Idempotency.
- Failure signals.
- Consistency/recovery.

### `openapi.yaml`

Starter skeleton cho synchronous API contract.

### `asyncapi.yaml`

Starter skeleton cho asynchronous event contract.

### `data-design.md`

Skeleton cho conceptual model, ownership, lifecycle, consistency và identifiers.

### `migration-plan.md`

Skeleton cho migration strategy, validation, rollback, coexistence và cleanup.

### `design-review.md`

Skeleton cho verdict, findings, driver coverage, consistency và scope limits.

### `sa-config.yaml`

Optional preferences:

- Mode.
- Language.
- Docs root.
- Diagram syntax.
- Contract versions.

Template là điểm bắt đầu, không phải form bắt buộc phải điền mọi section.

---

## 8. `examples/` — executable learning example

### `examples/README.md`

Map của example, giải thích tại sao mỗi artifact tồn tại.

### `examples/express-lane/sa-config.yaml`

Minh họa optional configuration. Example vẫn có thể được tạo nếu file này không tồn tại.

### `examples/express-lane/architecture-brief.md`

Root artifact của example. Các file khác phải nhất quán với problem, drivers và recommendation trong brief.

### `decisions/ADR-0001-async-order-intake.md`

Ghi lại quyết định decouple acceptance khỏi fulfilment.

### `hld/container-orders.puml`

Static container structure.

### `hld/container-orders-catalogue.md`

Responsibility, ownership, contract và failure behaviour của elements/relationships.

### `flows/client-submit-express-order.puml`

Runtime proof cho happy path, retries, failures, durability và DLQ.

### `interfaces/order-intake-api.yaml`

OpenAPI contract cho clients và internal state update.

### `interfaces/order-intake-events.yaml`

AsyncAPI contract cho `order.accepted`.

### `data/data-design.md`

Single-writer ownership, lifecycle và coexistence.

### `reviews/design-review-2026-03-14.md`

Review report dựa trên đúng các artifact tồn tại trong example.

## 9. `docs/` — tài liệu dành cho con người

### `docs/sa-learning-guide.md`

Giải thích phương pháp SA, input/output từng bước, cách đọc example và lộ trình luyện tập.

### `docs/repository-layout-guide.md`

File hiện tại. Dùng để hiểu cấu trúc và trách nhiệm của từng nhóm file trong plugin repository.

Khác biệt quan trọng:

- `docs/` giúp người dùng học và maintain plugin.
- `skills/` là instruction cho Claude.
- `templates/` là skeleton cho project artifact.
- `examples/` là output mẫu.

---

## 10. `scripts/` — deterministic tooling

### `scripts/validate_repo.py`

Kiểm tra:

- Plugin manifest.
- Skill surface.
- Skill frontmatter.
- Internal references.
- Example inventory.
- Review references.
- PlantUML marker balance.
- YAML parsing.
- Local `$ref` resolution.

Chạy bằng:

```bash
python3 scripts/validate_repo.py
```

Tác dụng: chuyển những rule cơ học thành automated checks thay vì hy vọng AI hoặc reviewer nhớ kiểm tra.

---

## 11. Skill repository và project output khác nhau thế nào?

Repository này chứa phương pháp và templates. Khi plugin được dùng trong một project khác, output thường nằm trong project đó:

```text
target-project/
└── docs/architecture/
    ├── architecture-brief.md
    ├── decisions/
    │   └── ADR-0001-....md
    ├── hld/
    │   └── container-....puml
    ├── flows/
    │   └── ....puml
    ├── interfaces/
    │   └── ....yaml
    ├── data/
    │   └── data-design.md
    └── reviews/
        └── design-review-....md
```

Không nhầm hai loại file:

| File trong plugin | File trong project đích |
|---|---|
| `skills/adr/SKILL.md` | Instruction để Claude tạo ADR |
| `templates/adr.md` | Skeleton ADR |
| `docs/architecture/decisions/ADR-....md` | ADR thật của project |
| `examples/.../ADR-....md` | ADR mẫu để học/test |

---

## 12. Dependency map giữa artifact

| Artifact | Input chính | Output được dùng bởi |
|---|---|---|
| Architecture brief | Requirements, evidence, constraints | Tất cả artifact chuyên biệt |
| ADR | Brief, drivers, options, existing ADRs | HLD, flow, interface, review |
| HLD | Brief, accepted ADRs | Flow, interface, data, review |
| Flow | Brief, HLD, ADRs, contracts | Interface, data, review |
| Interface | Brief, consumers, flow, data vocabulary | Delivery teams, review |
| Data design | Brief, HLD, flows, contracts | Interface, migration, review |
| Review | Tất cả artifact liên quan | Corrective work và readiness decision |

Interface và data có thể co-evolve. Nếu interface cần field mới, data ownership phải được xác nhận; nếu data classification thay đổi, contract có thể phải loại hoặc bảo vệ field.

---

## 13. Khi thêm hoặc thay đổi một skill

Checklist maintainer:

1. Tạo hoặc sửa `skills/<name>/SKILL.md`.
2. Đặt toàn bộ trigger information trong frontmatter description.
3. Giữ body ngắn; chỉ reference standard/template cần thiết.
4. Tạo standard nếu artifact có quality rules riêng.
5. Tạo template nếu output có cấu trúc lặp lại.
6. Cập nhật `skills/method/SKILL.md` nếu routing thay đổi.
7. Cập nhật README và docs nếu user-facing surface thay đổi.
8. Thêm hoặc sửa example để chứng minh workflow.
9. Cập nhật validator nếu inventory thay đổi.
10. Chạy:

```bash
python3 scripts/validate_repo.py
claude plugin validate .
git diff --check
```

---

## 14. Thư mục rỗng

Các folder rỗng còn lại từ phiên bản skill cũ đã được loại bỏ khỏi working directory. Git vốn không track thư mục rỗng; layout chính thức của plugin được xác định bởi các file thực sự tồn tại, đặc biệt là `skills/*/SKILL.md` và validator inventory.
