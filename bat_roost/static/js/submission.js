$(document).ready(function(){
    let status_change_url = glob_status_url;
    let csrf_token = glob_csrf_token;
    let preloader ='<div class="preloader-wrapper small active"><div class="spinner-layer spinner-blue-only"><div class="circle-clipper left"><div class="circle"></div></div><div class="gap-patch"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div>'

    $(".accept-submission").on("click", function(){
        let id=$(this).data("id");
        let review=$("#review").val();
        $("#action"+id).html(preloader);
        $.ajax({
            type: 'POST',
            url: status_change_url,
            data: {
                "id":id,
                "csrfmiddlewaretoken":csrf_token,
                "status":"AC",
                "review":review,
            },
            datatype: 'json',
            success: function(response){
                console.log(response)
               if(response.success==true){
                   $("#action"+id).empty();
                   $("#status"+id).text(response.status_display);
                   location.reload(true);
               }
               else{
                   console.log("Failed");
               }
            }
        });
    });

    $(".reject-submission").on("click", function(){
        let id=$(this).data("id");
        let review=$("#review").val();
        $("#action"+id).html(preloader);
        $.ajax({
            type: 'POST',
            url: status_change_url,
            data: {
                "id":id,
                "csrfmiddlewaretoken":csrf_token,
                "status":"RJ",
                "review":review,
            },
            datatype: 'json',
            success: function(response){
                console.log(response)
                if(response.success==true){
                    $("#action"+id).empty();
                    $("#status"+id).text(response.status_display);
                    location.reload(true);
                }
                else{
                }
                    console.log("Failed");
            }
        });
    });

})
