# Hướng dẫn học Solution Architecture với `skill-sa`

Để hiểu cây thư mục và trách nhiệm của từng file trong repository, xem thêm [`repository-layout-guide.md`](repository-layout-guide.md).

## 1. Solution Architect thực sự làm gì?

Solution Architect không chỉ vẽ sơ đồ hệ thống. Vai trò chính là biến một yêu cầu mơ hồ thành một thiết kế có thể:

- Giải thích được tại sao chọn giải pháp này.
- Chứng minh được giải pháp đáp ứng nhu cầu quan trọng.
- Chỉ rõ ranh giới, trách nhiệm và ownership.
- Làm rõ hành vi khi hệ thống lỗi.
- Tạo contract để các team làm việc độc lập.
- Phát hiện rủi ro trước khi implementation bắt đầu.

Luồng tư duy tổng quát:

```text
Business problem và evidence
          ↓
   Architecture brief
          ↓
  Có cần artifact chuyên biệt?
    ├─ Quyết định khó đảo ngược → ADR
    ├─ Cần hiểu cấu trúc        → HLD
    ├─ Runtime phức tạp         → Flow
    ├─ Có consumer khác team    → Interface
    └─ Data qua boundary        → Data design
          ↓
  Architecture review
          ↓
Implementation-ready direction
```

Đây không phải waterfall. HLD, flow, interface và data thường được làm lặp qua lại.

Ví dụ:

- Khi vẽ flow, bạn phát hiện API thiếu idempotency.
- Khi thiết kế data, bạn phát hiện hai service cùng ghi một entity.
- Khi viết contract, bạn phát hiện thay đổi là breaking.
- Khi review, bạn phát hiện HLD và ADR đang nói hai điều khác nhau.

SA giỏi không tránh iteration; SA giỏi làm cho iteration diễn ra trước khi code đã quá đắt để sửa.

---

## 2. Bốn loại input mà một SA cần thu thập

### 2.1. Business input

Bao gồm:

- Vấn đề hiện tại là gì?
- Ai bị ảnh hưởng?
- Chi phí của vấn đề là gì?
- Outcome cần đạt là gì?
- Deadline do đâu?
- Ai là decision maker?
- Ai có quyền veto?
- Điều gì nằm ngoài scope?

Ví dụ tốt:

> Tỷ lệ duplicate order giờ cao điểm là 1.9%, mỗi duplicate mất 12 phút xử lý thủ công.

Ví dụ chưa đủ:

> Cần cải thiện order system.

### 2.2. Technical evidence

Bao gồm:

- Source code hiện tại.
- API specifications.
- Database schemas.
- Deployment topology.
- Metrics và production dashboards.
- Incident reports.
- Existing ADRs.
- Architecture diagrams.
- Ý kiến từ system owner.

Một SA phải phân biệt:

- **Fact:** được chứng minh bằng evidence.
- **Assumption:** đang tin là đúng nhưng chưa xác minh.
- **Open question:** thiếu thông tin và có người cần trả lời.

### 2.3. Constraints

Constraint là điều giới hạn solution space:

- Phải chạy trên Kubernetes hiện tại.
- Không được chuyển dữ liệu ra khỏi Việt Nam.
- Phải dùng identity provider hiện tại.
- Không thể downtime.
- Chỉ có ba tháng delivery.
- Team chưa có kinh nghiệm vận hành Kafka.

Constraint khác preference:

- “Công ty bắt buộc dùng PostgreSQL” là constraint.
- “Team thích PostgreSQL” là preference.

SA phải làm rõ vì hai loại này có sức nặng khác nhau.

### 2.4. Architecture drivers

Driver là điều thật sự làm thay đổi cấu trúc hệ thống.

Ví dụ:

- p99 latency < 800 ms tại 500 concurrent requests.
- Hệ thống vẫn nhận order khi fulfilment down.
- Không được mất order đã acknowledge: RPO = 0.
- Duplicate rate < 0.01%.
- Một team phải deploy độc lập.
- Data phải lưu trong region.

Nếu bỏ một requirement mà kiến trúc không đổi, requirement đó có thể không phải architecture driver.

---

## 3. Input/output của từng bước

## Bước 1 — `/sa:architect`

Skill: [`skills/architect/SKILL.md`](../skills/architect/SKILL.md)

Đây là entry point mặc định. Người dùng không cần biết trước mình cần ADR, HLD hay flow.

### Input

- Yêu cầu của người dùng.
- Business context.
- Requirement documents hoặc ticket.
- Repository/source code liên quan.
- Existing architecture documents.
- Constraints.
- Production evidence.
- `sa-config.yaml` nếu có, nhưng không bắt buộc.

### Việc `architect` thực hiện

1. Hiểu vấn đề.
2. Xác định scope.
3. Tách fact, assumption và open question.
4. Xác định ba đến năm driver quan trọng nhất.
5. Phân tích current state và impact.
6. Đưa ra hai hoặc ba option thật.
7. So sánh trade-off.
8. Đề xuất solution.
9. Quyết định có cần artifact chuyên biệt không.

### Ba loại output

#### `quick`

Output chỉ nằm trong conversation.

Dùng khi:

- Cần tư vấn.
- Cần đánh giá một ý tưởng.
- Cần so sánh hai giải pháp.
- Chưa cần lưu thiết kế lâu dài.

Ví dụ:

```text
/sa:architect Chúng tôi nên dùng event hay synchronous API cho payment confirmation?
```

#### `brief`

Output mặc định:

```text
docs/architecture/architecture-brief.md
```

Template: [`architecture-brief.md`](../skills/method/templates/architecture-brief.md)

Dùng khi nhiều người cần thống nhất:

- Vấn đề gì đang được giải quyết?
- Tại sao solution này được chọn?
- Boundaries chính là gì?
- Những gì còn chưa quyết định?

#### `artifact`

`architect` route sang skill chuyên biệt:

- Quyết định → `/sa:adr`
- Cấu trúc → `/sa:hld`
- Hành vi runtime → `/sa:flow`
- Contract → `/sa:interface`
- Data ownership/migration → `/sa:data`
- Đánh giá thiết kế → `/sa:review`

### Kỹ năng SA được luyện

- Problem framing.
- Stakeholder analysis.
- Scope control.
- Architecture driver identification.
- Option analysis.
- Trade-off communication.
- Đưa ra recommendation có điều kiện.

---

## Bước 2 — Architecture Brief

Template: [`architecture-brief.md`](../skills/method/templates/architecture-brief.md)

Đây là artifact trung tâm của flow mới.

### Input

- Business problem.
- Stakeholders.
- Constraints.
- Metrics.
- Current architecture.
- Source code và existing contracts.
- Assumptions.
- Candidate options.

### Output

Một file bao gồm mười nhóm thông tin.

### 1. Problem and outcome

Trả lời:

- Hiện tại có vấn đề gì?
- Ai bị ảnh hưởng?
- Hậu quả đo được là gì?
- Sau khi hoàn thành, điều gì phải tốt hơn?

Không nên viết solution ở phần problem.

Sai:

> Chúng ta cần Kafka để giảm latency.

Đúng:

> Acknowledgement latency phụ thuộc fulfilment và vượt timeout của client.

### 2. Scope

Phải có cả:

- In scope.
- Out of scope.

Out-of-scope quan trọng vì nó bảo vệ design khỏi tiếp tục mở rộng.

### 3. Drivers and constraints

Mỗi driver nên có:

- Tên.
- Target hoặc tác động.
- Source.

Ví dụ:

| Driver | Target |
|---|---|
| Acknowledgement latency | p99 < 800 ms |
| Availability | Vẫn accept khi fulfilment down |
| Data loss | RPO = 0 |

### 4. Current state and impact

Không mô tả toàn bộ hệ thống. Chỉ mô tả phần liên quan đến thay đổi.

Phải trả lời:

- Component nào bị thay đổi?
- Consumer nào bị ảnh hưởng?
- Data nào đổi ownership hoặc schema?
- Team nào cần phối hợp?
- Operational burden nào được thêm vào?

### 5. Options and recommendation

Đây là nơi thể hiện chất lượng reasoning của SA.

Một comparison tốt không chỉ viết:

| Option | Score |
|---|---|
| A | 8 |
| B | 6 |

Nó phải giải thích lý do:

- Option nào đáp ứng driver nào?
- Option nào không thể đáp ứng?
- Operational cost?
- Delivery risk?
- Reversibility?
- Điều gì sẽ làm recommendation thay đổi?

### 6. Proposed architecture

Mô tả:

- Các responsibility chính.
- Boundaries.
- Integration style.
- Deployment direction.
- Runtime flow quan trọng.

Architecture brief không cần chứa mọi chi tiết. Chi tiết khó hiểu được tách sang HLD hoặc flow.

### 7. Interfaces and data

Trả lời:

- Ai cung cấp contract?
- Ai consume?
- Entity do ai sở hữu?
- Consistency là strong hay eventual?
- Lifecycle hoặc retention là gì?

### 8. Cross-cutting concerns

Ít nhất phải suy nghĩ qua:

- Security.
- Resilience.
- Observability.
- Cost.
- Delivery.

Không phải concern nào cũng cần một tài liệu riêng. Nhưng không được quên xem xét.

### 9. Decisions, risks and open questions

Đây là “unfinished business” của thiết kế.

Phân biệt:

- **Decision:** đã hoặc cần chọn.
- **Risk:** sự kiện có thể xảy ra và gây hậu quả.
- **Assumption:** điều đang tin nhưng chưa chứng minh.
- **Open question:** thiếu câu trả lời.

### 10. Next steps

Không viết một danh sách chung chung. Nên chỉ rõ hành động nhỏ nhất tiếp theo:

- Chốt ADR.
- Xác nhận consumer.
- Viết API spec.
- Chạy load test.
- Làm review.

### Tác dụng của architecture brief

Nó là “single narrative” giúp product, engineering, operations và architecture hiểu cùng một câu chuyện.

Nếu chỉ có HLD mà không có brief, người xem biết hệ thống gồm những box nào nhưng không biết:

- Vì sao chúng tồn tại?
- Driver nào khiến chúng xuất hiện?
- Option nào đã bị loại?
- Scope là gì?
- Rủi ro còn lại là gì?

---

## Bước 3 — `/sa:adr`

Skill: [`skills/adr/SKILL.md`](../skills/adr/SKILL.md)  
Template: [`templates/adr.md`](../skills/method/templates/adr.md)  
Standard: [`adr.md`](../skills/method/standards/adr.md)

ADR là Architecture Decision Record.

### Input

- Architecture brief hoặc requirements liên quan.
- Drivers quyết định lựa chọn.
- Constraints.
- Affected design.
- Existing ADRs.
- Các option đã xem xét.
- Người có quyền quyết định.

### Output

```text
docs/architecture/decisions/ADR-NNNN-<slug>.md
```

### Một ADR tốt phải trả lời

1. Câu hỏi quyết định là gì?
2. Context nào khiến quyết định khó?
3. Có những option nào?
4. Option nào được chọn?
5. Vì sao?
6. Hậu quả tiêu cực là gì?
7. Có thể đảo ngược không?
8. Khi nào nên xem xét lại?
9. Làm sao kiểm tra system vẫn tuân theo quyết định?

### Tại sao một ADR chỉ chứa một quyết định?

Ví dụ không tốt:

> Chọn Kafka, PostgreSQL, Kubernetes và microservices.

Bốn quyết định này có lifecycle khác nhau. Sau này có thể thay Kafka nhưng giữ PostgreSQL. Nếu chúng nằm chung một ADR thì không thể supersede độc lập.

### Status

- `Proposed`: chưa được authorised deciders chấp thuận.
- `Accepted`: đã thống nhất.
- `Rejected`: option không được chọn hoặc đề xuất bị bác.
- `Superseded`: có ADR mới thay thế.

Claude không được tự suy ra `Accepted`.

### Kỹ năng SA được luyện

- Decision framing.
- Phân tích option công bằng.
- Viết consequence.
- Reversibility thinking.
- Architecture governance.

---

## Bước 4 — `/sa:hld`

Skill: [`skills/hld/SKILL.md`](../skills/hld/SKILL.md)  
Standard: [`hld.md`](../skills/method/standards/hld.md)  
Diagram conventions: [`diagrams.md`](../skills/method/standards/diagrams.md)

HLD trả lời: hệ thống có những phần nào và chúng liên hệ ra sao?

### Input

- Architecture brief.
- Accepted ADRs.
- Existing diagrams.
- Current system boundaries.
- External systems.
- Team ownership.
- Trust boundaries.
- Data ownership direction.

### Output

Tùy view:

```text
docs/architecture/hld/system-context.puml
docs/architecture/hld/container-<system>.puml
docs/architecture/hld/component-<container>.puml
docs/architecture/hld/deployment-<environment>.puml
```

Có thể thêm catalogue:

```text
docs/architecture/hld/<view>-catalogue.md
```

Template: [`hld-catalogue.md`](../skills/method/templates/hld-catalogue.md)

### Các level của C4

#### System Context

Audience:

- Business.
- Product.
- Management.
- Technical teams mới tham gia.

Trả lời:

- Hệ thống là gì?
- Ai sử dụng?
- Giao tiếp với hệ thống bên ngoài nào?

Không nên chứa service, database hoặc class.

#### Container View

“Container” trong C4 không nhất thiết là Docker container. Nó là một runnable/deployable unit hoặc data store:

- Web application.
- Backend service.
- Database.
- Queue.
- Mobile application.
- Serverless function.

Đây là view mặc định vì nó thể hiện architecture boundary hữu ích nhất.

#### Component View

Cho thấy bên trong một container.

Chỉ dùng khi internals thực sự có ý nghĩa kiến trúc. Nếu mọi class đều xuất hiện, nó đã trở thành detailed design.

#### Deployment View

Standard: [`deployment-view.md`](../skills/method/standards/deployment-view.md)

Trả lời:

- Container chạy ở đâu?
- Region/AZ nào?
- Có bao nhiêu instance?
- Failure domain là gì?
- Traffic đi qua network boundary nào?
- Ingress/egress?
- Shared infrastructure?
- Scaling mechanism?

### HLD catalogue để làm gì?

Diagram nên dễ đọc. Vì vậy thông tin chi tiết được đưa vào catalogue.

#### Elements table

- Element.
- Responsibility.
- Owner.
- Data hoặc contract.

#### Relationships table

- From → to.
- Mechanism.
- Purpose.
- Failure behaviour.

Catalogue ngăn việc tạo một diagram chứa quá nhiều text.

### Structural checks

SA phải kiểm tra:

- Circular dependency.
- Quá nhiều synchronous hop.
- Excessive fan-out.
- Chatty calls.
- Shared database.
- Component không có responsibility rõ ràng.
- Component không liên quan driver nào.
- Hai team cùng sở hữu một deployable unit.

### Kỹ năng SA được luyện

- System decomposition.
- Boundary design.
- Coupling/cohesion.
- Ownership.
- Trust boundary.
- Deployment topology.
- Communicating architecture visually.

---

## Bước 5 — `/sa:flow`

Skill: [`skills/flow/SKILL.md`](../skills/flow/SKILL.md)  
Standard: [`runtime-flow.md`](../skills/method/standards/runtime-flow.md)  
Template narrative: [`flow-narrative.md`](../skills/method/templates/flow-narrative.md)

HLD mô tả static structure. Flow mô tả hành vi theo thời gian.

### Input

- Architecture brief.
- HLD.
- Relevant ADRs.
- Existing API/event contracts.
- Timeout hoặc availability drivers.
- Failure assumptions.

### Output

```text
docs/architecture/flows/<flow-name>.puml
```

Có thể thêm:

```text
docs/architecture/flows/<flow-name>.md
```

Narrative chỉ cần khi diagram không thể thể hiện rõ operational detail.

### Một flow tốt phải có

#### Trigger và preconditions

Điều gì bắt đầu flow và điều gì phải đúng trước đó?

Ví dụ:

> Client submits an order sau khi authenticate và tạo idempotency key.

#### Participants

Tên phải khớp HLD.

Nếu HLD dùng `order-intake` mà flow dùng `order-api`, người đọc không biết đó là một hay hai component.

#### Happy path

Các bước thành công, đánh số rõ ràng.

#### Failure paths

Ít nhất phải xem xét:

- Invalid input.
- Authentication/authorisation failure.
- Dependency timeout.
- Dependency unavailable.
- Retry.
- Duplicate request.
- Duplicate event.
- Partial completion.
- Poison message.
- Out-of-order event.
- Resource exhaustion.

#### Timeout và retry

Retry không mặc định là tốt.

Ví dụ nguy hiểm:

```text
POST /payment → timeout → retry
```

Nếu operation không idempotent, retry có thể charge hai lần.

SA phải trả lời:

- Timeout là bao nhiêu?
- Retry mấy lần?
- Backoff?
- Operation có idempotent không?
- Deduplication key là gì?
- Tổng timeout có vượt caller deadline không?

#### Consistency points

Flow phải cho biết:

- Khi nào state trở nên durable?
- Khi nào user được acknowledgement?
- Eventual consistency kéo dài bao lâu?
- User nhìn thấy gì trong khoảng đó?

#### Compensation/reconciliation

Nếu nhiều bước không thể transaction atomically:

- Có rollback không?
- Có saga không?
- Có reconciliation job không?
- Có manual recovery không?

#### Observability points

Flow không cần biến thành monitoring document, nhưng phải chỉ ra:

- Step nào cần metric?
- Failure nào cần alert?
- Correlation ID đi thế nào?
- Queue lag được đo ở đâu?

### Kỹ năng SA được luyện

- Distributed systems thinking.
- Failure-oriented design.
- Timeout budgeting.
- Retry/idempotency.
- Eventual consistency.
- Recovery and observability.

---

## Bước 6 — `/sa:interface`

Skill: [`skills/interface/SKILL.md`](../skills/interface/SKILL.md)  
Standard: [`interface.md`](../skills/method/standards/interface.md)  
Templates: [`openapi.yaml`](../skills/method/templates/openapi.yaml), [`asyncapi.yaml`](../skills/method/templates/asyncapi.yaml)

Interface là boundary giữa hai team hoặc hai hệ thống.

### Input

- Architecture brief.
- Relevant flow.
- Consumer list.
- Consumer outcome.
- Domain vocabulary.
- Data sensitivity.
- Existing API/event specs.
- Migration constraints.

### Output

Synchronous:

```text
docs/architecture/interfaces/<name>-api.yaml
```

Asynchronous:

```text
docs/architecture/interfaces/<name>-events.yaml
```

### Nguyên tắc consumer-first

Không bắt đầu từ database table hoặc Java class.

Sai:

> Có bảng `orders`, vậy tạo CRUD API cho tất cả columns.

Đúng:

> Mobile client cần submit order và kiểm tra trạng thái; fulfilment cần idempotently cập nhật processing state.

Mỗi operation phải có:

- Consumer cụ thể.
- Outcome cụ thể.

Operation không có consumer là dấu hiệu over-design.

### OpenAPI cần quyết định

- Resource model.
- Status codes.
- Error format.
- Authentication.
- Scopes.
- Rate limits.
- Payload size.
- Pagination.
- Idempotency.
- Versioning.
- Deprecation.
- Examples.
- Sensitive fields.

### AsyncAPI cần quyết định

- Event là fact hay command?
- Producer.
- Consumers.
- Envelope.
- Event name.
- Delivery semantics.
- Ordering.
- Partition key.
- Retention.
- Replay.
- Schema compatibility.
- Deduplication.
- DLQ/poison-message behaviour.

### Compatibility per consumer

Một schema change không tự động là breaking hoặc non-breaking. Phải đánh giá từ góc nhìn consumer.

Ví dụ thêm required field có thể:

- Không breaking cho producer.
- Breaking cho consumer validator.
- Breaking cho stored event replay.
- Không breaking cho consumer tolerant reader.

### Kỹ năng SA được luyện

- Boundary design.
- Consumer-driven thinking.
- API governance.
- Event semantics.
- Backward compatibility.
- Migration planning.

---

## Bước 7 — `/sa:data`

Skill: [`skills/data/SKILL.md`](../skills/data/SKILL.md)  
Standard: [`data.md`](../skills/method/standards/data.md)  
Template: [`data-design.md`](../skills/method/templates/data-design.md)  
Migration template: [`migration-plan.md`](../skills/method/templates/migration-plan.md)

### Input

- Architecture brief.
- HLD.
- Significant flows.
- Existing contracts.
- Current data documentation.
- Regulatory requirements.
- Current volumes/growth nếu chúng ảnh hưởng design.

### Output

```text
docs/architecture/data/data-design.md
```

Nếu có existing data thay đổi:

```text
docs/architecture/data/migration-plan.md
```

### Data design giải quyết gì?

#### Conceptual model

Tập trung vào domain:

- Order.
- Customer.
- Payment.
- Shipment.

Không tập trung vào:

- Index.
- Partition.
- Column type chi tiết.
- Query tuning.

Đó thường là implementation design.

#### Ownership

Mỗi entity phải có một authoritative owner.

Ownership không chỉ là “database nằm ở team nào”. Nó trả lời:

- Ai được quyền thay đổi state?
- Ai enforce invariant?
- Ai publish authoritative event?
- Ai quyết định lifecycle?
- Consumer khác truy cập qua contract nào?

Hai component cùng write một entity là một architecture decision cần được làm rõ.

#### Classification

Nhận diện:

- PII.
- Confidential data.
- Restricted data.
- Regulatory tags.
- Data residency.

#### Lifecycle

- Ai tạo?
- Ai mutate?
- Retention bao lâu?
- Khi nào archive?
- Khi nào delete?
- Legal basis?

#### Consistency

Đối với relationship qua boundary:

- Strong consistency?
- Eventual consistency?
- Tolerated window?
- Outbox, saga, CDC hay reconciliation?
- User nhìn thấy gì trong inconsistency window?

#### Migration

Một migration plan tốt phải có:

- Strategy.
- Ordered steps.
- Validation.
- Rollback.
- Point of no return.
- Coexistence source of truth.
- Conflict resolution.
- End date.
- Cleanup owner.

“Dual-write một thời gian” chưa phải migration plan nếu không có reconciliation và ngày kết thúc.

### Kỹ năng SA được luyện

- Domain modelling.
- Data ownership.
- Consistency models.
- Privacy and retention.
- Migration/coexistence.
- Source-of-truth reasoning.

---

## Bước 8 — `/sa:review`

Skill: [`skills/review/SKILL.md`](../skills/review/SKILL.md)  
Standard: [`review.md`](../skills/method/standards/review.md)  
Template: [`design-review.md`](../skills/method/templates/design-review.md)

Review không phải “tôi thấy thiết kế này ổn”. Nó là evidence-based judgement.

### Input

- Architecture brief.
- ADRs trong scope.
- HLD.
- Runtime flows.
- Interface specs.
- Data design.
- Relevant repository evidence.
- Driver targets.

Không cần mọi artifact phải tồn tại. Nếu một artifact không cần thiết, review không được report nó là missing.

### Output

Conversation findings hoặc:

```text
docs/architecture/reviews/design-review-<date>.md
```

### Mười chiều review

1. Problem và scope.
2. Driver satisfaction.
3. Cross-artifact consistency.
4. Security/privacy.
5. Resilience.
6. Observability/operability.
7. Simplicity.
8. Cost proportionality.
9. Deployment/migration feasibility.
10. Buildability.

### Driver coverage

Không chỉ hỏi “driver có được mention không”. Phải chỉ ra mechanism:

| Driver | Mechanism |
|---|---|
| RPO 0 | Commit order và outbox trong một transaction trước acknowledgement |
| Accept khi fulfilment down | Fulfilment không nằm trên synchronous path |
| Deduplicate retry | Unique idempotency key và trả lại original order |

### Finding severity

- `Blocker`: không thể build an toàn hoặc critical driver không thể đạt.
- `Major`: có khả năng gây incident hoặc rework đáng kể.
- `Minor`: nên sửa nhưng không block.
- `Observation`: lời khuyên không vi phạm rule rõ ràng.

Verdict:

- Có Blocker → `NOT READY`.
- Không Blocker nhưng có Major → `READY WITH CONDITIONS`.
- Không có Blocker/Major → `READY`.

### Review không sửa design

Review chỉ đưa findings về cho owner.

Nếu reviewer tự sửa design, ranh giới giữa author và reviewer biến mất. Reviewer dễ “sửa cho qua” thay vì chỉ rõ lỗ hổng.

### Kỹ năng SA được luyện

- Critical thinking.
- Evidence-based review.
- Consistency analysis.
- Risk classification.
- Communicating corrective actions.
- Independent judgement.

---

## 4. Tác dụng của các nhóm file trong repo

### 4.1. `skills/*/SKILL.md`

Đây là instruction cho Claude, không phải deliverable của dự án.

Một `SKILL.md` có hai lớp.

#### Frontmatter

```yaml
name: architect
description: ...
allowed-tools: Read, Grep, Glob
```

`description` là phần quan trọng nhất để Claude quyết định khi nào skill trigger.

#### Body

Chứa:

- Input cần đọc.
- Method.
- Output.
- Standard/template cần dùng.
- Boundary của skill.

Nói cách khác:

- `description` quyết định **có dùng skill hay không**.
- Body quyết định **dùng skill như thế nào**.

### 4.2. Shared method

File: [`skills/method/SKILL.md`](../skills/method/SKILL.md)

Đây là shared operating contract. Nó định nghĩa:

- Bảy core skill.
- Ba mode `quick`, `brief`, `artifact`.
- Minimal workflow.
- Quality rules chung.
- Optional config.
- Reference routing.

Tác dụng chính là tránh lặp cùng một rule trong bảy skill.

### 4.3. `standards/`

Standards trả lời:

> Một artifact tốt phải có gì?

| File | Tác dụng |
|---|---|
| `core-flow.md` | Sơ đồ core flow và promotion trigger |
| `workflow.md` | Cách Claude hiểu, scope, produce và report |
| `adr.md` | Quality bar cho quyết định |
| `hld.md` | Quality bar cho cấu trúc hệ thống |
| `runtime-flow.md` | Quality bar cho runtime behaviour |
| `interface.md` | Quality bar cho API/event contract |
| `data.md` | Quality bar cho data ownership/migration |
| `review.md` | Review dimensions và verdict |
| `diagrams.md` | Quy tắc C4, PlantUML, sequence/data diagram |
| `quality-bar.md` | Quality rules chung |
| `tailoring.md` | Khi nào quick, brief hoặc artifact |
| `deployment-view.md` | Region, node, network, scaling, failure domain |
| `operating-guardrails.md` | Evidence, write scope, review independence |

Các số bị thiếu như 02, 03, 04 là do repo giữ stable numbering sau khi rút gọn. Không có nghĩa là flow hiện tại bị thiếu bước.

### 4.4. `templates/`

Templates trả lời:

> Artifact nên có hình dạng nào?

| Template | Output |
|---|---|
| `architecture-brief.md` | Design baseline tổng hợp |
| `adr.md` | Decision record |
| `hld-catalogue.md` | Element và relationship metadata |
| `deployment-catalogue.md` | Node/network deployment information |
| `flow-narrative.md` | Runtime detail bổ sung cho sequence diagram |
| `openapi.yaml` | Synchronous API contract |
| `asyncapi.yaml` | Event contract |
| `data-design.md` | Ownership, lifecycle, consistency |
| `migration-plan.md` | Migration/coexistence |
| `design-review.md` | Review report |
| `sa-config.yaml` | Optional project preferences |

Template không phải form bắt buộc điền hết. Nếu section không liên quan, bỏ hoặc ghi rõ `N/A` khi việc vắng mặt cần được hiểu.

### 4.5. Plugin metadata

[`plugin.json`](../.claude-plugin/plugin.json) định nghĩa:

- Tên plugin: `sa`.
- Version.
- Description.
- Author.
- Keywords.

[`marketplace.json`](../.claude-plugin/marketplace.json) giúp Claude marketplace discover và install plugin.

Hai file này không chứa architecture method; chúng là packaging metadata.

### 4.6. Validator

File: [`scripts/validate_repo.py`](../scripts/validate_repo.py)

Validator kiểm tra:

- Có đúng tám `SKILL.md`.
- Skill name khớp folder.
- Internal references tồn tại.
- Plugin manifest hợp lệ.
- Example có đúng file.
- Review không trỏ file bị thiếu.
- PlantUML marker cân bằng.
- YAML parse được.
- Local `$ref` resolve được.

Đây là ví dụ của một nguyên tắc SA quan trọng:

> Việc nào có thể kiểm tra cơ học thì không nên chỉ dựa vào lời nhắc cho AI hoặc review thủ công.

---

## 5. Phân tích example `express-lane`

Example map: [`examples/README.md`](../examples/README.md)

### 5.1. Architecture brief

File: [`architecture-brief.md`](../examples/express-lane/architecture-brief.md)

Đây là root artifact. Nó xác định:

- Problem: acknowledgement chậm vì chờ fulfilment.
- Outcome: accept nhanh và không mất order.
- Drivers: latency, availability, duplicate prevention.
- Options: async, optimise sync, do nothing.
- Recommendation: transactional outbox và Kafka.
- Cross-cutting concerns.
- Risks và next actions.

Mọi artifact khác phải nhất quán với brief này.

### 5.2. ADR-0001

File: [`ADR-0001-async-order-intake.md`](../examples/express-lane/decisions/ADR-0001-async-order-intake.md)

Tách riêng vì async acceptance là:

- Hard to reverse.
- Cross-team.
- Làm thay đổi contract semantics.
- Thêm operational burden.
- Ảnh hưởng nhiều artifact downstream.

ADR không mô tả toàn bộ design. Nó chỉ bảo tồn quyết định “decouple acceptance from fulfilment”.

### 5.3. Container diagram

File: [`container-orders.puml`](../examples/express-lane/hld/container-orders.puml)

Cho thấy:

- `order-intake`.
- `order-events`.
- `orders-db`.
- `fulfilment-service`.
- `recon-batch`.
- Sync vs async relationships.

Nó trả lời “các phần nào tồn tại”.

### 5.4. HLD catalogue

File: [`container-orders-catalogue.md`](../examples/express-lane/hld/container-orders-catalogue.md)

Bổ sung:

- Responsibility.
- Owner.
- Contract.
- Failure behaviour.
- Structural checks.

Nó trả lời “mỗi arrow thực sự có nghĩa gì”.

### 5.5. Runtime flow

File: [`client-submit-express-order.puml`](../examples/express-lane/flows/client-submit-express-order.puml)

Chứng minh solution hoạt động qua:

- Happy path.
- Duplicate retry.
- Database failure.
- Publish failure.
- Fulfilment outage.
- Poison message.
- Terminal outcomes.

Đây là nơi ADR “async acceptance” được kiểm chứng về mặt hành vi.

### 5.6. OpenAPI contract

File: [`order-intake-api.yaml`](../examples/express-lane/interfaces/order-intake-api.yaml)

Định nghĩa:

- `POST /orders`.
- `GET /orders/{orderId}`.
- Internal state update.
- `Idempotency-Key`.
- 202 semantics.
- OIDC scopes.
- Error model.

Đây là contract để client và fulfilment team implement độc lập.

### 5.7. AsyncAPI contract

File: [`order-intake-events.yaml`](../examples/express-lane/interfaces/order-intake-events.yaml)

Định nghĩa:

- Event `order.accepted`.
- Producer.
- Consumer.
- Payload.
- Delivery semantics.
- Partition key.
- Retention.
- Deduplication responsibility.

### 5.8. Data design

File: [`data-design.md`](../examples/express-lane/data/data-design.md)

Giải quyết một điểm rất quan trọng:

> Chỉ `order-intake` được ghi Order.

`fulfilment-service` không ghi trực tiếp database. Nó dùng internal API.

Nhờ đó:

- Business invariant có một owner.
- Không có shared-write schema coupling.
- API có thể enforce state transition.
- Audit và idempotency tập trung.

### 5.9. Design review

File: [`design-review-2026-03-14.md`](../examples/express-lane/reviews/design-review-2026-03-14.md)

Review tìm thấy:

- Thiếu executable DLQ drain procedure → Major.
- Alert threshold chưa được load-test → Minor.

Verdict là `READY WITH CONDITIONS`, không phải `READY`, vì failure recovery chưa hoàn chỉnh.

### 5.10. Optional config

File: [`sa-config.yaml`](../examples/express-lane/sa-config.yaml)

Chỉ chứa preference:

- Mode.
- Language.
- Docs root.
- Diagram syntax.
- Contract versions.

Nó không gate skill và không bắt buộc tồn tại.

---

## 6. Cách học SA bằng repo này

### Giai đoạn 1 — Học problem framing

Chọn một feature nhỏ trong hệ thống thực tế.

Chạy:

```text
/sa:architect Phân tích thay đổi này ở quick mode. Chưa tạo file.
```

Tự trả lời:

- Problem thật là gì?
- Outcome gì được đo?
- Ai bị ảnh hưởng?
- Scope nào cần loại?
- Fact nào có evidence?
- Assumption nào đang tồn tại?

Mục tiêu: không nhảy ngay vào technology.

### Giai đoạn 2 — Viết architecture brief

Yêu cầu:

```text
/sa:architect Tạo architecture brief cho thay đổi này.
```

Sau đó tự review:

- Có ít nhất hai option thật không?
- Recommendation có deciding trade-off không?
- Negative consequence có rõ không?
- Có “what would change the decision” không?

### Giai đoạn 3 — Viết ADR

Chọn một quyết định:

- Sync hay async.
- Build hay buy.
- Shared service hay team-owned service.
- New database hay reuse existing.
- Batch hay streaming.

Thử viết ADR mà không dùng các câu:

- “Best practice”.
- “Industry standard”.
- “Scalable”.
- “Modern”.

Thay bằng driver và evidence.

### Giai đoạn 4 — HLD

Vẽ container diagram tối đa khoảng 8–12 element.

Với mỗi box hỏi:

- Responsibility?
- Owner?
- Data?
- Deployment reason?
- Driver nào khiến box này tồn tại?

Với mỗi arrow hỏi:

- Direction?
- Purpose?
- Protocol?
- Sync/async?
- Timeout?
- Failure behaviour?

### Giai đoạn 5 — Failure-oriented flow

Chọn một flow quan trọng rồi viết failure path trước happy path:

- Database down.
- Queue down.
- Duplicate request.
- Duplicate event.
- Timeout.
- Partial completion.
- Poison message.

Đây là bài tập rất tốt để chuyển từ developer thinking sang architect thinking.

### Giai đoạn 6 — Contract và data

Tự đặt câu hỏi:

- Consumer thật sự là ai?
- Consumer cần outcome nào?
- Có breaking change không?
- Ai sở hữu entity?
- Ai được write?
- Retention?
- Eventual consistency có visible effect gì?
- Migration rollback thế nào?

### Giai đoạn 7 — Independent review

Đợi một vài ngày hoặc mở session mới rồi chạy:

```text
/sa:review Review design này như thể bạn không tham gia tạo nó.
```

Không chỉ đọc finding. Hãy tự trả lời trước khi xem kết quả:

- Critical driver được đáp ứng bằng mechanism nào?
- Artifact có mâu thuẫn không?
- Failure nào chưa có recovery?
- Complexity nào không được driver biện minh?
- Team có thể bắt đầu implementation mà không cần thêm architecture decision không?

---

## 7. Những lỗi người mới làm SA thường gặp

1. Chọn technology trước khi hiểu problem.
2. Vẽ diagram nhưng không có decision basis.
3. NFR chỉ có tính từ, không có số.
4. Mọi quality attribute đều được đánh High.
5. Chỉ thiết kế happy path.
6. Retry mà không có idempotency.
7. Hai service cùng write một database entity.
8. API được tạo trực tiếp từ database schema.
9. Event name mô tả command nhưng được gọi là event.
10. ADR chỉ có một option.
11. Không viết negative consequences.
12. Migration không có rollback hoặc end date.
13. Review dựa trên cảm giác, không có evidence.
14. Tạo mọi artifact vì template tồn tại.
15. Thiết kế vượt xa nhu cầu của change.

---

## 8. Tóm tắt lộ trình tư duy SA

```text
Hiểu vấn đề
  → xác định driver
  → so sánh option
  → ghi quyết định
  → mô hình hóa structure
  → mô hình hóa behaviour
  → cố định contract và ownership
  → review bằng evidence
```

Nếu chỉ nhớ một nguyên tắc, hãy nhớ:

> Mỗi thành phần kiến trúc phải tồn tại vì một driver, mỗi boundary phải có owner và contract, và mỗi quyết định quan trọng phải nói rõ cái giá phải trả.
