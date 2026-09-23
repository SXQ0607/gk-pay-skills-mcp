# gk-pay-skills-mcp —— 付费技能 MCP Server（0.05 元/次，支付宝 A2M）

把 13 个「支付宝 A2M 按量 0.05 元」付费端点打包成标准 MCP Server，可一键提交到各大 MCP 市场，白嫖发现流量，且 402/按量计费照常运转。

## 本地运行

```bash
pip install -r requirements.txt
python server.py          # 默认 stdio 模式
# 或 HTTP/SSE 模式（便于远程托管）：
python server.py --transport streamable-http --host 0.0.0.0 --port 8000
```

## 计费模型（重要）
- 全部工具无 Payment-Proof 调用 → 服务端返回 **HTTP 402 + Payment-Needed 账单头**（金额 0.05，收款链接 `API_B1409FBC01A84610`）。
- 调用方用 `alipay-bot 402-buyer-pay` 完成支付，再用 `402-query-payment-status` 带 Payment-Proof 重调即得业务结果。
- 这跟腾讯 SkillPay / 支付宝 Skill Pay 同为「调用即扣费」模型，但**分成 100% 归己、无需微信商户号**。

## 工具清单（13 个）
diagnose / calc / plc_annotate / term_map / viral_hook / a_share_morning / bazi_quick /
ecom_selling_copy / novel_outline_studio / toutiao_killer_title / xhs_viral_note /
xianyu_listing_pro / ziwei_life_read

---

## 逐平台铺货执行清单（"搞平台"行动表）

状态：✅ 我已可直接干  🟡 需你授权/账号  ⏸️ 暂观望

| # | 平台 | 动作 | 所需条件 | 状态 |
|---|---|---|---|---|
| 1 | **SkillHub（腾讯）** | 已上架 12 个 pay slug，全 0.05 | 已就绪 | ✅ 完成 |
| 2 | **MCP 官方 Registry** | 推 GitHub + `mcp-publisher` 发布 | 需 GitHub 仓库（可我建） | 🟡 待你给仓库或授权 |
| 3 | **Smithery** | `smithery mcp publish` 一键托管 | Smithery 账号（免费） | 🟡 待账号 |
| 4 | **Glama** | 加 `mcp-server` topic 被爬取 + claim | GitHub 仓库 | 🟡 同 #2 |
| 5 | **mcp.so** | 网页表单提交 | 免费 | ✅ 我可填（需你确认品牌信息） |
| 6 | **PulseMCP** | 从官方 Registry 自动同步 | 同 #2 | 🟡 同 #2 |
| 7 | **mcpservers.org** | 网页提交 | 免费 | ✅ 我可填 |
| 8 | **SkillPie (skillpie.cn)** | 发布 Skill（无企业认证） | 平台账号 | 🟡 待账号 |
| 9 | **Capafy** | 云端运行 Skill 按次收费 | 平台账号 + 逻辑上云 | 🟡 待账号 |
| 10 | **Coze 扣子 技能商店** | 上架付费技能（已有 1 元订单案例） | 抖音/字节账号 + 企业或个人 | 🟡 待账号 |
| 11 | **钉钉悟空 Skill 市场** | 企业内分发 | 企业钉钉组织 | 🟡 待组织 |
| 12 | **支付宝 AI 开放平台 / A2M** | 一次接入多端分发 | 已自建 A2M，可对接「AI收」 | ✅ 已具备，可加深 |
| 13 | **蚂蚁 Agentar** | 金融 B 端智能体 | 企业资质 | ⏸️ 暂观望 |
| 14 | **豆包 / 千问 智能体商店** | 分成型分发 | 字节/阿里账号 | 🟡 待账号 |

### 我此刻能零凭证推进的
- ✅ 本 MCP Server 已构建并通过 402 实测（见下）。
- ✅ mcp.so / mcpservers.org 网页表单提交（只需你点头，我代填，但品牌/联系方式需你定）。
- ✅ 把 13 端点再包装成「可直接 `git clone` 运行的 GitHub 仓库结构」以待 #2/#3/#4/#5 提交。

### 需你拍板的
1. **GitHub 仓库**：是否要我把这个 server 推到一个 GitHub 仓（用于官方 Registry/Glama/Smithery 自动同步）？给仓库地址或授权我建。
2. **mcp.so / mcpservers.org 提交**：是否现在就代填提交？需你确认展示用的**联系邮箱/主页**。
3. **账号类平台（Smithery/Coze/SkillPie/Capafy）**：要不要我整理一份「逐平台注册+上架 SOP」给你，你注册后我接管上架？

## 本地验证
```python
from server import _call
print(_call("/api/diagnose", {"brand":"g120","symptom":"F07452"}))
# 期望: {'status': 402, 'payment_needed': '...', 'amount_cny': 0.05, ...}
```

mcp-name: io.github.SXQ0607/gk-pay-skills-mcp
