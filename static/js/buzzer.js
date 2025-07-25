let buzzerState = true; // true = 켜짐, false = 꺼짐

function buzzerSwitchHandler() {
    const label = document.getElementById("buzzerLabel");

    // 상태 토글(켜져있으면 꺼지고, 꺼져있으면 켜짐)
    buzzerState = !buzzerState;

    //서버에 fetch 요청보내기
    const state = buzzerState ? "on" : "off";

    fetch(`/dashboard/buzzer?state=${state}`)
    .then(response => response.json())
    .then(data => {
        label.textContent = buzzerState ? "BUZZER ON" : "BUZZER OFF";
    })
    .catch(error => {
        console.error("BUZZER 전송 실패", error)
        label.textContent = "에러";
    });
}

document.getElementById("buzzerSwitch").addEventListener("change", buzzerSwitchHandler); 