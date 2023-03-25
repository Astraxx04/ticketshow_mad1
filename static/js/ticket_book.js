var booking_venue = sessionStorage.getItem("booking_venue");
var booking_show = sessionStorage.getItem("booking_show");





function tot_price() 
{
    var seats = document.getElementById('num_seats').value;
    var total = seats * document.getElementById('price').value;
    document.getElementById('total').value = total;
    console.log(total);
}