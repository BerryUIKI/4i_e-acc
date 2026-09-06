use serde::Serialize;
use tauri_plugin_dialog::DialogExt;

#[derive(Serialize)]
struct AppInfo {
    name: &'static str,
    version: &'static str,
    local: bool,
}

/// Basic app metadata shown by the desktop shell.
/// No network, no telemetry — everything stays on this machine.
#[tauri::command]
fn app_info() -> AppInfo {
    AppInfo {
        name: "Quadruple Leverage Toolbox",
        version: env!("CARGO_PKG_VERSION"),
        local: true,
    }
}

/// Save `content` to a user-picked location via a native save dialog.
/// Returns the written path, or "cancelled" if the dialog was dismissed.
#[tauri::command]
fn export_result(
    app: tauri::AppHandle,
    content: String,
    default_name: String,
) -> Result<String, String> {
    let path = app
        .dialog()
        .file()
        .set_file_name(default_name)
        .add_filter("CSV / Text", &["csv", "txt"])
        .blocking_save_file();
    match path {
        Some(tauri_plugin_dialog::FilePath::Path(p)) => {
            std::fs::write(&p, content).map_err(|e| format!("write failed: {e}"))?;
            Ok(p.to_string_lossy().into_owned())
        }
        Some(_) => Err("unsupported destination".to_string()),
        None => Ok("cancelled".to_string()),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![app_info, export_result])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
