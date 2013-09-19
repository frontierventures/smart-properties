$(document).ready(function(){
    $('.fiat_amount').text(0);         
    var last = $('input[name=last]').val();

    //$('div#rateFiat').on('keyup', 'input[name=loanAmountFiat]', function (e) {             
    //    var value = $('div#rateFiat').find(this).val();             
    //    $('div#rateBtc').find('input[name=btc_loan_amount]').css("background-color", "white");             
    //    var result = Math.round(100000000 * value / last) / 100000000;             
    //    $('div#rateBtc').find('input[name=btc_loan_amount]').val(result);         
    //});         
    //$('div#rateFiat').on('keydown', 'input[name=loanAmountFiat]', function (e) {             
    //    $('div#rateBtc').find('input[name=btc_loan_amount]').css("background-color", "gold");         
    //});                  

    $('div#rateBtc').on('keyup', 'input[name=btc_loan_amount]', function (e) {             
        var value = $('div#rateBtc').find(this).val();             
        $('div#rateFiat').find('input[name=loanAmountFiat]').css("background-color", "white");             
        var result = value * last;             
        //$('div#rateFiat').find('input[name=loanAmountFiat]').val(result);         
        $('.fiat_amount').text(result);         
    });         
    $('div#rateBtc').on('keydown', 'input[name=btc_loan_amount]', function (e) {             
        $('div#rateFiat').find('input[name=loanAmountFiat]').css("background-color", "gold");         
    });
});
