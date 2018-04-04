$(document).ready(function() {
var miles = 0;
var open = false;
var distanceArr;
var dateArr;
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
      url: "http://174.50.170.196/run.php", //Relative or absolute path to response.php file
      success: function(data) {
        miles = 0;
        distanceArr = [];
        dateArr = [];
        appendStr = "";
        Object.keys(data).forEach(function(key) {
          console.log(data[key]);
          miles += parseFloat(data[key].miles);

          distanceArr.push(data[key].miles);
          dateArr.push(data[key].day);
        });
        $("#miles").html(miles.toFixed(2));
        $("#mileDistance").html(miles.toFixed(2)+" miles<span style='font-size: 4vmin;'>Current Distance</span>");
        for (let i = 0; i < dateArr.length; i++) {
          appendStr+=('\
            <tr style="color:black;">\
              <td style="color:black;">'+dateArr[i]+'</td>\
              <td>'+distanceArr[i]+'</td>\
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
      url: "http://174.50.170.196/modal.php", //Relative or absolute path to response.php file
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


