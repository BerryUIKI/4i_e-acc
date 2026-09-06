use serde::Serialize;

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

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![app_info])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
