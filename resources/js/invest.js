$(document).ready(function(){
    var last = $('input[name=last]').val();

    $('div#rateFiat').on('keyup', 'input[name=investmentAmountFiat]', function (e) {             
        var value = $('div#rateFiat').find(this).val();             
        $('div#rateBtc').find('input[name=investmentAmountBtc]').css("background-color", "white");             
        var result = Math.round(100000000 * value / last) / 100000000;             
        $('div#rateBtc').find('input[name=investmentAmountBtc]').val(result);         
    });         
    $('div#rateFiat').on('keydown', 'input[name=investmentAmountFiat]', function (e) {             
        $('div#rateBtc').find('input[name=investmentAmountBtc]').css("background-color", "gold");         
    });                  

    $('div#rateBtc').on('keyup', 'input[name=investmentAmountBtc]', function (e) {             
        var value = $('div#rateBtc').find(this).val();             
        $('div#rateFiat').find('input[name=investmentAmountFiat]').css("background-color", "white");             
        var result = value * last;             
        $('div#rateFiat').find('input[name=investmentAmountFiat]').val(result);         
    });         
    $('div#rateBtc').on('keydown', 'input[name=investmentAmountBtc]', function (e) {             
        $('div#rateFiat').find('input[name=investmentAmountFiat]').css("background-color", "gold");         
    });
});
