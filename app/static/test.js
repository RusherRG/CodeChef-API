$(document).ready(function() {

    $('.updateButton').on('click', function() {

        req = $.ajax({
            url : '/update',
            type : 'POST',
            data : { name : "name"}
        });

        req.done(function(data) {

            $('.testp').fadeOut(1000).fadeIn(1000);
            $('.testp').text('Ranking :' + data.rank);

        });
    

    });

});

$(document).ready(function() {

    $('.addfriend').on('click', function() {
        
        var fname = $('#input_friend').val();
        
        req = $.ajax({
            url : '/addFriend',
            type : 'POST',
            data : { fname : fname}
        });

        req.done(function(data) {

            //$('.ffullname').text(data.ffullname);
            //$('.fusername').text(data.fusername);
            //$('.forg').text(data.forg);
            //$('.frating').text(data.frating);
            if(data == 'SomeWrong')
            {
                var x = document.getElementById("snackbar");
                x.innerHTML = "Something Went Very Wrong :(";
                // Add the "show" class to DIV
                x.style.backgroundColor="#333";
                x.className = "show";

                // After 3 seconds, remove the show class from DIV
                setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

            }
            else if(data == 'UserNE'){
                    /*var erBox = document.getElementById('modalFsInfo');
                    erBox.style.display = "block";
                    erBox.className = "red darken-3 white-text";
                    erBox.innerHTML = "Uh oh. Sorry but that user does not exist.";
                    setTimeout(function(){ erBox.style.display = "none"; }, 5000);*/
                    var x = document.getElementById("snackbar");
                    document.getElementById("snackbar").innerHTML = "Uh oh. Sorry but that user does not exist.";
                    // Add the "show" class to DIV
                    x.style.backgroundColor="#c62828";
                    x.className = "show";
                    
                    // After 3 seconds, remove the show class from DIV
                    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
            }
            else if(data == 'UserAF')
            {
                    /*var erBox = document.getElementById('modalFsInfo');
                    erBox.style.display = "block";
                    erBox.className = erBox.className.replace("red darken-3", "");
                    erBox.className = "blue darken-3 white-text";
                    erBox.innerHTML = "That user is already your friend";
                    setTimeout(function(){ erBox.style.display = "none"; }, 5000);*/
                    var x = document.getElementById("snackbar");
                    document.getElementById("snackbar").innerHTML = "That user is already your friend.";
                    x.style.backgroundColor="#01579b";
                    x.className = "show";
                    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
            }else{
            $('#friendlist').prepend(data);
            
            // Get the snackbar DIV
            var erBox = document.getElementById('modalFsInfo');
            erBox.style.display = "none";
            $('#modal1').modal('close');
            var x = document.getElementById("snackbar");
            document.getElementById("snackbar").innerHTML = "Friend Added Successfully";
            // Add the "show" class to DIV
            x.style.backgroundColor="#333";
            x.className = "show";

            // After 3 seconds, remove the show class from DIV
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
            }

            document.getElementById('input_friend').value = "";

        });
    

    });

});

$(document).ready(function() {

    //var countContest = document.getElementById('contestLen').innerHTML;
    var countContest = document.getElementById('ongoingContestTitle').dataset.countcontest;
    var dateArr=[];
    for(var i = 0; i<countContest; i++)
    {
           // dateArr.push(new Date(document.getElementById('contest'+i).innerHTML));
           dateArr.push(new Date(document.getElementById('contest'+i).dataset.endtime));
    }

    // Update the count down every 1 second
    var x = setInterval(function() {

        // Get todays date and time
        var now = new Date().getTime();
        for(var i = 0; i<dateArr.length; i++){
            var countDownDate = dateArr[i];
        // Find the distance between now and the count down date
        var distance = countDownDate - now;
    
        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
        // Display the result in the element with id="demo"
        document.getElementById("contest"+i+"out").innerHTML = days + "d " + hours + "h "
        + minutes + "m " + seconds + "s ";

        }
    
        
    }, 1000);
});



