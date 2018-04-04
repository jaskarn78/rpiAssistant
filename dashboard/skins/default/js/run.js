$(document).ready(function() {
var open = false;
var appendStr;
$('.slider').slick({
  infinite: true,
  slidesToShow: 1,
  slidesToScroll: 1,
  autoplay: true
});
getRunData();
setInterval(getRunData, 5000);

function getRunData(){
    $.ajax({
      type: "GET",
      dataType: "json",
      url: "http://jaskarndev.com/Dashboard/skins/default/php/run.php", //Relative or absolute path to response.php file
      success: function(data) {
        var miles = 0;
        var distanceArr = [];
        var dateArr = [];
        var timeArr = [];
        appendStr = "";
        Object.keys(data).forEach(function(key) {
          console.log(data[key]);
          miles += parseFloat(data[key].miles);
          if(parseFloat(data[key].miles) % 1 != 0)
            distanceArr.push(data[key].miles);
          else
            distanceArr.push(data[key].miles+".00");
          dateArr.push(data[key].day);
          timeArr.push(parseFloat(data[key].time));
           
        });
        $("#miles").html(miles.toFixed(2));
        $("#mileDistance").html(miles.toFixed(2)+" miles<span style='font-size: 4vmin;'>Current Distance</span>");
        for (let i = 0; i < dateArr.length; i++) {
          appendStr+=('\
            <tr style="color:black;">\
              <td style="color:black;">'+dateArr[i]+'</td>\
              <td>'+distanceArr[i]+'</td>\
              <td>'+timeArr[i]+'</td>\
            </tr>');
        }
        $(".runData").html(appendStr);
      }
    });
}

setInterval(function(){ 
  $.ajax({
      type: "GET",
      dataType: "json",
      url: "http://jaskarndev.com/Dashboard/skins/default/php/modal.php", //Relative or absolute path to response.php file
      success: function(data) {
        if(parseInt(data[0].value) == 1){
           $('.modal').addClass('active');
           open = true;
        } else{
          $('.modal').removeClass('active');
        }
      }
    });
}, 1000);


});


