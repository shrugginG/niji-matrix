"""Serialize conclusion-scoped source records for the two visual-capture candidates."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
H = {tid: yaml.safe_load((RUN / f"{tid}-handoff.yaml").read_text(encoding="utf-8")) for tid in ("T1113", "T1125")}

# ID, candidate, research key, filename, bilingual title, source type,
# publisher, and source-specific evidentiary scope. URLs are taken unchanged
# from the reviewed handoff; unsupported stealth axes remain planning-only.
SOURCES = [
    ("REF-000666", "T1113", "T1113_REF_ATTACK", "mitre-t1113-screen-capture", "屏幕捕获，技术 T1113", "Screen Capture, Technique T1113", "official-documentation", "MITRE ATT&CK", "锚定固定版父行为、Collection 映射与零子项；不能独立证明匿迹变量。", "Anchors fixed parent behavior, Collection mapping, and zero children; does not independently establish stealth."),
    ("REF-000667", "T1113", "T1113_REF_VOLEXITY", "volexity-bluelight-screen-cadence", "Volexity 对 BLUELIGHT 截图节奏的分析", "North Korean APT InkySquid Infects Victims Using Browser Exploits", "incident-report", "Volexity", "记录截图间隔变化；没有证明降低告警、匿迹意图或跨阈值效果。", "Records a screenshot cadence change, not reduced alerts, evasive intent, or a crossed threshold."),
    ("REF-000668", "T1113", "T1113_REF_MITRE_DET", "mitre-screen-capture-detection", "ATT&CK 屏幕捕获检测策略", "Detection Strategy for Screen Capture", "official-documentation", "MITRE ATT&CK", "提供截图行为与产物关联线索；具体平台字段须独立核验。", "Provides screen-capture and artifact correlation clues; exact platform fields require separate verification."),
    ("REF-000669", "T1113", "T1113_REF_SYSMON", "microsoft-sysmon-configuration-files", "Microsoft Sysmon 配置与事件采集说明", "Sysmon Configuration Files", "official-documentation", "Microsoft Learn", "支撑已配置文件、进程及模块事件的前提；普通窗口查询或像素取得并非默认 Sysmon 事件。", "Supports configured file, process, and module events; ordinary window queries and pixel acquisition are not default Sysmon events."),
    ("REF-000670", "T1113", "T1113_REF_MS_WGC", "microsoft-windows-graphics-capture", "Windows Graphics Capture 屏幕采集说明", "Screen Capture in Windows Apps", "official-documentation", "Microsoft Learn", "说明该 API 的用户选择与黄色边框；不能外推到 GDI、CopyFromScreen 或所有截图方法。", "Documents this API's picker and yellow border, not GDI, CopyFromScreen, or every capture path."),
    ("REF-000671", "T1113", "T1113_REF_APPLE_SCREEN", "apple-screen-recording-permission", "Apple 屏幕录制访问管理", "Control Access to Screen and System Audio Recording on Mac", "official-documentation", "Apple Support", "说明 macOS 应用屏幕录制授权；平台界面不等于可查询企业审计流。", "Describes macOS app screen-recording grants; the privacy UI is not a guaranteed queryable enterprise audit stream."),

    ("REF-000672", "T1125", "T1125_REF_ATTACK", "mitre-t1125-video-capture", "视频捕获，技术 T1125", "Video Capture, Technique T1125", "official-documentation", "MITRE ATT&CK", "锚定固定版摄像头及通话视频输入、间隔帧、Collection 映射和零子项；图片后缀不决定分类。", "Anchors fixed camera and call-video input, interval frames, Collection mapping, and zero children; image extension does not classify the source."),
    ("REF-000673", "T1125", "T1125_REF_ZOOM", "objective-see-zoom-camera-grant-lab", "Objective-See 对 Zoom 相机授权继承的实验", "Zoom Camera Permission Inheritance Research", "vendor-report", "Objective-See", "实验中注入库继承旧 macOS Zoom 相机权限并录到短片；非野外恶意案例。", "An injected library inherited older macOS Zoom camera permission and recorded a short clip in a lab; not a field malware case."),
    ("REF-000674", "T1125", "T1125_REF_WARDLE", "wardle-existing-webcam-stream-lab", "Wardle 对既有摄像头流寄生录制的研究", "Getting Duped: Piggybacking Webcam Streams for Surreptitious Recordings", "academic-paper", "Virus Bulletin", "说明旧平台既有摄像头会话的实验性寄生风险；不能证明本批候选的野外实施。", "Documents a laboratory risk of piggybacking an existing webcam stream on an older platform; not observed deployment here."),
    ("REF-000675", "T1125", "T1125_REF_MS_CAM", "microsoft-camera-microphone-privacy", "Windows 摄像头和麦克风隐私控制", "Windows Camera, Microphone, and Privacy", "official-documentation", "Microsoft Support", "说明用户摄像头权限与可见性，不能单凭授权断言有视频产物。", "Documents user camera grants and visibility; authorization alone does not establish video output."),
    ("REF-000676", "T1125", "T1125_REF_APPLE_CAM", "apple-media-capture-authorization", "macOS 媒体采集授权", "Requesting Authorization for Media Capture on macOS", "official-documentation", "Apple Developer", "说明首次相机授权及后续复用；不证明恶意接口附着或录制。", "Explains first camera grant and later reuse; does not establish malicious interface attachment or recording."),
    ("REF-000677", "T1125", "T1125_REF_APPLE_IND", "apple-camera-indicator", "Apple 摄像头使用指示", "Use Control Center on Mac", "official-documentation", "Apple Support", "说明 macOS 摄像头绿色指示及应用显示；不能外推为所有端点都有集中日志。", "Describes the macOS camera indicator and app display; not a universal centralized event log."),
]

def source(tactic, key):
    return next(x for x in H[tactic]["library_candidates"]["references"]
                if x.get("key") == key or x.get("temporary_key") == key)

for rid, tactic, key, slug, zh, en, kind, publisher, note_zh, note_en in SOURCES:
    item = source(tactic, key)
    path = ROOT / "references" / f"{rid}-{slug}.yaml"
    record = {"schema_version": "1.0.0", "type": "reference", "id": rid,
              "title_zh": zh, "title_en": en, "source_type": kind,
              "authors": [publisher], "publisher": publisher, "published": None,
              "url": item["url"], "accessed": "2026-09-22", "locator": item.get("locator") or note_en,
              "archive_url": None, "credibility": "high", "notes_zh": note_zh, "notes_en": note_en}
    path.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

print("Serialized 12 visual-capture source records")
