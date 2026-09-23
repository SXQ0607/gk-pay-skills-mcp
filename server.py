#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gk-pay-skills-mcp —— 工控 & 通用付费技能 MCP Server
====================================================
把 13 个「支付宝 A2M 按量 0.05 元」付费端点暴露为 MCP 工具。
提交到 Smithery / Glama / mcp.so / 官方 Registry 等 MCP 市场后，
任何接入这些市场的 Agent 都能发现并调用本服务；调用无 Payment-Proof 时
服务端返回 HTTP 402 + 账单（Payment-Needed 头），由 alipay-bot 完成支付后重调即得结果。

所有工具统一返回：
  - status 200 + data：已带 Payment-Proof 或已付费时的业务结果
  - status 402 + payment_needed：待支付的账单（base64url），交给 alipay-bot 402-buyer-pay
"""
from fastmcp import FastMCP
import requests

BASE = "https://gk-diagnose-308980-8-1461759720.sh.run.tcloudbase.com"
TIMEOUT = 30

mcp = FastMCP("gk-pay-skills-mcp")


def _call(path: str, params: dict):
    """统一请求：无凭证→402 账单；有凭证→业务结果。"""
    try:
        r = requests.get(BASE + path, params=params, timeout=TIMEOUT)
    except requests.RequestException as e:
        return {"status": "error", "message": f"请求失败: {e}"}
    if r.status_code == 402:
        bill = r.headers.get("Payment-Needed")
        return {
            "status": 402,
            "payment_needed": bill,
            "amount_cny": 0.05,
            "收款链接 service_id": "API_B1409FBC01A84610",
            "hint": "将 payment_needed 交给 alipay-bot 402-buyer-pay 完成支付，"
                    "再用 402-query-payment-status 带 Payment-Proof 重调本工具即得 data。",
        }
    try:
        payload = r.json()
    except ValueError:
        payload = {"raw": r.text}
    return {"status": r.status_code, "data": payload}


@mcp.tool()
def skill_catalog() -> dict:
    """列出全部 13 个付费技能及其价格（均为 0.05 元/次，支付宝 A2M 按量）。用于发现可用能力。"""
    catalog = [
        {"name": "diagnose", "desc": "工控故障排查诊断（g120/s7/fx5u/hmi/modbus）", "price": 0.05},
        {"name": "calc", "desc": "选型估算：电缆截面/断路器/电机电流", "price": 0.05},
        {"name": "plc-annotate", "desc": "PLC 变量表中文注释生成", "price": 0.05},
        {"name": "term-map", "desc": "工控术语对照映射", "price": 0.05},
        {"name": "viral-hook", "desc": "爆款钩子生成", "price": 0.05},
        {"name": "a-share-morning", "desc": "A股财经早报复盘", "price": 0.05},
        {"name": "bazi-quick", "desc": "八字快速解读", "price": 0.05},
        {"name": "ecom-selling-copy", "desc": "电商卖点文案", "price": 0.05},
        {"name": "novel-outline-studio", "desc": "小说大纲工坊", "price": 0.05},
        {"name": "toutiao-killer-title", "desc": "头条爆款标题", "price": 0.05},
        {"name": "xhs-viral-note", "desc": "小红书种草笔记", "price": 0.05},
        {"name": "xianyu-listing-pro", "desc": "闲鱼高转化商品文案", "price": 0.05},
        {"name": "ziwei-life-read", "desc": "紫微斗数命盘解读", "price": 0.05},
    ]
    return {"total": len(catalog), "unit_price_cny": 0.05, "pay_protocol": "支付宝 A2M / 402", "skills": catalog}


@mcp.tool()
def diagnose(brand: str, symptom: str) -> dict:
    """工控故障排查诊断。输入设备品牌与故障现象，返回按匹配度排序的排查方案。每次 ¥0.05。
    brand: 设备品牌，如 g120 / s7-1200 / fx5u / hmi / modbus
    symptom: 故障现象，如 F07452 / 通讯不通 / 启动不转 / 报警灯闪"""
    return _call("/api/diagnose", {"brand": brand, "symptom": symptom})


@mcp.tool()
def calc(type: str, power: float, voltage: float = 380.0, length: float = 50.0) -> dict:
    """选型估算（三相 380V 基准，经验公式）。每次 ¥0.05。
    type: cable 电缆截面 | breaker 断路器 | motor 电机电流
    power: 功率 kW（必填，>0）
    voltage: 电压 V（默认 380）
    length: 长度 m（电缆用，默认 50）"""
    return _call("/api/calc", {"type": type, "power": power, "voltage": voltage, "length": length})


@mcp.tool()
def plc_annotate(vars: str) -> dict:
    """PLC 变量表中文注释生成。输入变量名列表（逗号分隔），返回中文注释映射。每次 ¥0.05。
    vars: 如 Motor1_Run,Valve3_Open,Emergency_Stop,Fault_Light"""
    return _call("/api/plc-annotate", {"vars": vars})


@mcp.tool()
def term_map(q: str) -> dict:
    """工控术语对照映射。输入术语（如 定时器），返回中英文/别名对照。每次 ¥0.05。"""
    return _call("/api/term-map", {"q": q})


@mcp.tool()
def viral_hook(theme: str, platform: str) -> dict:
    """爆款钩子生成。输入主题与平台，返回开篇反常识钩子。每次 ¥0.05。
    theme: 如 PLC调试 / 副业 / 护肤
    platform: 如 抖音 / 小红书 / 头条"""
    return _call("/api/viral-hook", {"theme": theme, "platform": platform})


@mcp.tool()
def a_share_morning(q: str) -> dict:
    """A股财经早报复盘生成。输入盘面描述，返回结构化复盘。每次 ¥0.05。
    q: 如 沪指涨0.8% 半导体领涨 量能放大"""
    return _call("/api/a-share-morning", {"q": q})


@mcp.tool()
def bazi_quick(q: str) -> dict:
    """八字快速解读。输入十神/干支关键词（如 正官），返回简明解读。每次 ¥0.05。"""
    return _call("/api/bazi-quick", {"q": q})


@mcp.tool()
def ecom_selling_copy(q: str) -> dict:
    """电商卖点文案。输入产品与卖点，返回转化导向文案。每次 ¥0.05。
    q: 如 保温杯 长效保温12h 食品级316"""
    return _call("/api/ecom-selling-copy", {"q": q})


@mcp.tool()
def novel_outline_studio(q: str) -> dict:
    """小说大纲工坊。输入题材（如 都市重生），返回分章大纲。每次 ¥0.05。"""
    return _call("/api/novel-outline-studio", {"q": q})


@mcp.tool()
def toutiao_killer_title(q: str) -> dict:
    """头条爆款标题。输入话题（如 房贷利率下调），返回高点击标题组。每次 ¥0.05。"""
    return _call("/api/toutiao-killer-title", {"q": q})


@mcp.tool()
def xhs_viral_note(q: str) -> dict:
    """小红书种草笔记。输入产品/话题（如 平价护肤），返回种草笔记。每次 ¥0.05。"""
    return _call("/api/xhs-viral-note", {"q": q})


@mcp.tool()
def xianyu_listing_pro(q: str) -> dict:
    """闲鱼高转化商品文案。输入商品（如 九成新Switch），返回标题+描述。每次 ¥0.05。"""
    return _call("/api/xianyu-listing-pro", {"q": q})


@mcp.tool()
def ziwei_life_read(q: str) -> dict:
    """紫微斗数命盘解读。输入关键词（如 紫微/命宫），返回命理解读。每次 ¥0.05。"""
    return _call("/api/ziwei-life-read", {"q": q})


if __name__ == "__main__":
    mcp.run()
