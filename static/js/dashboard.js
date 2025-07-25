function sensorData() {
    fetch('/dashboard/data')
    .then(response => response.json())
    .then(data => {
       
        //정상적으로 값이 들어오면 
        if(data.temperature !== "Error" && data.humidity !== "Error"){
            document.getElementById("temp").textContent = data.temperature;
            document.getElementById("humid").textContent = data.humidity;
            document.getElementById("timestamp").textContent = data.timestamp;
        }
        // 비정상적인 값
        else{
            document.getElementById("temp").textContent = "온도 값 불러오기 실패";
            document.getElementById("humid").textContent = "습도 값 불러오기 실패";
        }
    })   
    .catch(error => {
        // 요청 실패 시 (서버 죽음, 연결 실패,... )
        console.error("Fetch Error", error);
        document.getElementById("temp").textContent = "에러";
        document.getElementById("humid").textContent = "에러";
    });

}
// 처음 로딩시 한번 실행 
//window.onload = function(){
    sensorData();

    //2초마다 실행
    setInterval(sensorData, 2000);
//};
