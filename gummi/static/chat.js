<script>
function passMessage(){
    $("form").bind("keypress", function(e) {
        if(e.keycode == 34)
        {
           $(".chat_content").append("$(\"textarea[name=message]\").val()");
        }
        });}
</script>
