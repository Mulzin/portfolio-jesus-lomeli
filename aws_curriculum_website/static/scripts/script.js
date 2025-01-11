const areaColor = {}
areaColor["Python"] = "#6F8FAF"
areaColor["WebDev"] = "#9F2B68"

function toggleContactVisibility(){
    var div = document.getElementById("toggleDiv");
    var mainDiv = document.getElementById("mainDiv");
    var state = window.getComputedStyle(document.getElementById("toggleDiv")).display;
    if(state == "flex"){
        div.style.display = "none";
        mainDiv.style.filter = 'blur(0px)';
    }else{
        div.style.display = "flex";
        mainDiv.style.filter = 'blur(5px)';
    }
}
function getProjects(){
    $.ajax({
        url: '/get_projects',
        type: 'GET',
        contentType: 'application/json',
        success: function fillName(response) {
            console.log(response)
            populateMainDiv(response)
        },
        error: function(error) {
            console.log(error)
        } 
    });
}       
function populateMainDiv(projectArray){
    var container = document.getElementById("mainDiv")

    for (let i in projectArray) {
        var projectDiv = document.createElement("div")
        projectDiv.classList.add("project-div")
        container.appendChild(projectDiv)

        var link = document.createElement("a")
        link.classList.add("project-link")
        link.href = projectArray[i][5]
        projectDiv.appendChild(link)

        var contentDiv = document.createElement("div")
        contentDiv.classList.add("project-content")  
        projectDiv.appendChild(contentDiv)
            
        var title = document.createElement("p")
        title.classList.add("project-title")
        title.innerHTML = projectArray[i][0]
        contentDiv.appendChild(title)

        var summary = document.createElement("p")
        summary.classList.add("project-summary")
        summary.innerHTML = projectArray[i][1]
        contentDiv.appendChild(summary)

        var area = document.createElement("p")
        area.classList.add("project-area")
        area.innerHTML = projectArray[i][3]
        area.style.backgroundColor = areaColor[projectArray[i][3]]
        contentDiv.appendChild(area)

        var imgDiv = document.createElement("div")
        imgDiv.classList.add("img-border")
        projectDiv.appendChild(imgDiv)

        var img = document.createElement("img")
        img.classList.add("project-img")
        var imgPath = projectArray[i][4]
        writeImgSrc(img,imgPath)

        imgDiv.appendChild(img)        
    }
}