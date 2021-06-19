var message_big_box = document.getElementById("content")
var empty = document.getElementById("empty")
var catch_box = message_big_box.getElementsByTagName("box")
var first_count = true
var now_count = 0


function loading(){
    fetch("/api/messages").then(function (response) {
        return response.json();
    }).then(function(result){
        let message_data = result["data"]
        if(message_data == ""){
            empty.textContent = "目前還沒有人到此一遊，快來寫下你的留言吧！"
        }
        let count=3; 
        if(first_count==false){
            if (now_count <= -1 ){
                alert("已經沒有留言了喔><!")
            } 
            else if(now_count-count<=-1){
                count = now_count+1
            }
        }
        else{
            now_count = message_data.length-1;
        }
        console.log(now_count)
        for(let j=0, i=now_count; j<count ; i--, j++){
            let message_name = document.createElement("div")
            let message_box = document.createElement("box")
            let message_text = document.createElement("div")
            let message_image = document.createElement("img")
            message_big_box.appendChild(message_box)
            message_name.textContent = message_data[i].name
            message_text.textContent = message_data[i].text
            message_name.className = "name";
            message_text.className = "text";
            message_image.setAttribute("src", message_data[i].image)
            message_image.className="image";
            message_box.appendChild(message_image)
            message_box.appendChild(message_name)
            message_box.appendChild(message_text)
        }
        now_count -= count;
        first_count = false;
    })
}


function submit(){
    let name = document.getElementById("input_name").value
    let text = document.getElementById("input_text").value;
    let image = document.getElementById("input_img").files;
    let image_test = document.getElementById("input_img").value;
    if(text != "" && name != ""){
        if(image_test == ""){
            image = ["copy"]
            var image_type = "copy"
        }
        else{
            var image_type = image[0].type
        }
        let formData = new FormData();
        formData.append('name', name);
        formData.append('text', text);
        formData.append('image', image[0]);
        formData.append('image_type', image_type);
        fetch("/api/message",{
            method: "POST",
            body: formData,
        }).then(function (response) {
            if(response.status === 200){
                downloading();                  
            }
            else if(response.status === 400){
                alert("訂單建立失敗，將自動整理頁面")
            }
            else{
                console.log("失敗")
            }
            return response.json();
        })
    }
    else{
        alert("尚未輸入暱稱或留言內容喔!")
    }
}

function downloading(){
    src = "/api/message"
    fetch(src).then(function (response) {
        return response.json();
    }).then(function(result){
        let message_box = document.createElement("box")
        let message_name = document.createElement("div")
        let message_text = document.createElement("div")
        let message_image = document.createElement("img")
        message_big_box.insertBefore(message_box, catch_box[0])
        message_name.textContent = result["data"][0].name
        message_text.textContent = result["data"][0].text
        message_name.className = "name";
        message_text.className = "text";
        message_image.setAttribute("src", result["data"][0].image)
        message_image.className = "image";
        message_box.appendChild(message_image)
        message_box.appendChild(message_name)
        message_box.appendChild(message_text)
    })
    empty.textContent = "";
}

function qrcode(){
    let qrcode = document.getElementById("qr_code");
    let qrbtn = document.getElementById("qr_btn")
    if(qrbtn.value=="Apple"){
        qrcode.setAttribute("src", "/static/image/qr_ios.png")
        qrbtn.textContent = "點擊切換GOOGLE PLAY"
        qrbtn.setAttribute("value", "Andorid")
    }
    else{
        qrcode.setAttribute("src", "/static/image/qr_andorid.png")
        qrbtn.textContent= "點擊切換APP STORE"
        qrbtn.setAttribute("value", "Apple")
    }

}

function checkfile(sender) {
    // 可接受的附檔名
    var validExts = new Array(".jpg", ".png", ".jpeg", ".bmp", ".tiff ", ".tif", ".gif");
  
    var fileExt = sender.value;
    fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
    if (validExts.indexOf(fileExt) < 0) {
      alert("檔案類型錯誤，僅接受圖片格式檔案");
      sender.value = null;
      return false;
    }
    else return true;
  }

loading();