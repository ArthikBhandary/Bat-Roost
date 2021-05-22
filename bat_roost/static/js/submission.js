$(document).ready(function(){
    let status_change_url = glob_status_url;
    let csrf_token = glob_csrf_token;
    let preloader ='<div class="preloader-wrapper small active"><div class="spinner-layer spinner-blue-only"><div class="circle-clipper left"><div class="circle"></div></div><div class="gap-patch"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div>'

    $(".accept-submission").on("click", function(){
        let id=$(this).data("id");
        $("#action"+id).html(preloader);
        $.ajax({
            type: 'POST',
            url: status_change_url,
            data: {
                "id":id,
                "csrfmiddlewaretoken":csrf_token,
                "status":"AC",
            },
            datatype: 'json',
            success: function(response){
                console.log(response)
               if(response.success==true){
                   $("#action"+id).empty();
                   $("#status"+id).text(response.status_display);
               }
               else{
                   console.log("Failed");
               }
            }
        });
    });

    $(".reject-submission").on("click", function(){
        let id=$(this).data("id");
        $("#action"+id).html(preloader);
        $.ajax({
            type: 'POST',
            url: status_change_url,
            data: {
                "id":id,
                "csrfmiddlewaretoken":csrf_token,
                "status":"RJ",
            },
            datatype: 'json',
            success: function(response){
                console.log(response)
                if(response.success==true){
                    $("#action"+id).empty();
                    $("#status"+id).text(response.status_display);
                }
                else{
                }
                    console.log("Failed");
            }
        });
    });

})
