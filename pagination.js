

var numbersOfItem = $('#item .card').length;
var limitPage=10;
$("#item .card:gt(" + (limitPage - 1) + ")").hide();
var totalPages=Math.ceil(numbersOfItem / limitPage)
$(".pagination").append( " <li id = 'Prev' class='page-item '> <span class='page-link'>  Previous  </span></li>");
$(".pagination").append( "<li class='page-link curent-page active'><a href='javascript:void(0)' >" + 1 + "</a> </li>");
for (var i = 2; i <= totalPages ; i++) {
  $(".pagination").append( "<li class='page-link curent-page'><a href='javascript:void(0)' >" + i + "</a> </li>");
}
console.log(totalPages)
$(".pagination").append("<li id = 'Next' class='page-item'><a class='page-link' href='javascript:void(0)'> Next  </a></li>");

$(".pagination li.curent-page").on("click",function (){
    if($(this).hasClass("active")){
        return false;
    }else{
        var currentPage = $(this).index();
        $(".pagination li").removeClass("active");
        $(this).addClass("active");
        $('#item .card').hide()
    }
    var grandTotal = limitPage * currentPage;
    for (var i = grandTotal - limitPage; i <grandTotal ; i++) {
        // $('#item .card:eq(' + i + ')').show();
        $("#item .card:eq(" + i + ")").show();
    }

});

$("#Next").on("click",function () {
    var currentPage = $(".pagination li.active").index();
    // alert(totalPages)
    if (currentPage == totalPages) {
        return false;
    } else {
        currentPage++;
        $(".pagination li").removeClass("active");
        $('#item .card').hide()
        var grandTotal = limitPage * currentPage;
        for (var i = grandTotal - limitPage; i < grandTotal; i++) {
            // $('#item .card:eq(' + i + ')').show();
            $("#item .card:eq(" + i + ")").show();
        }

        $(".pagination li.curent-page:eq(" + (currentPage - 1) + ")").show().addClass('active');
    }
});
$("#Prev").on("click",function () {
    var currentPage=$(".pagination li.active").index();
    // alert(totalPages)
    if (currentPage==1){
        return false;
    } else{
        currentPage--;
        $(".pagination li").removeClass("active");
        $('#item .card').hide()
        var grandTotal = limitPage * currentPage;
        for (var i = grandTotal - limitPage; i <grandTotal ; i++) {
        // $('#item .card:eq(' + i + ')').show();
        $("#item .card:eq(" + i + ")").show();
    }

        $(".pagination li.curent-page:eq(" + (currentPage-1) + ")").show().addClass('active');
    }

});
console.log(Math.ceil(12.1))