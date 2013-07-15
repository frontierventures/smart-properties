$(document).ready(function(){
    $("#orderStatus").change(function(){     
        window.location='../orders?status=' + this.value; 
    }); 
});
