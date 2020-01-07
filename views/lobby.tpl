% rebase('base.tpl', title='Lobby')
<script type="text/javascript">
var data = ["{{state}}", {{ready}}, {{player_count}}];

function refresh() {
    var request = new XMLHttpRequest();
    request.open('GET', 'status', true);

    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            var new_data = JSON.parse(this.response);

            if(new_data[0] != "WAITING"){
                window.location.href = "./map.cgi";
            }
            if(new_data[1] != data[1] || new_data[2] != data[2]){                
                window.location.reload(true);
            }

        } else {

        }
        setTimeout(refresh, 1000);
    };

    request.onerror = function() {
        setTimeout(refresh, 1000);
    };

    request.send();
}
setTimeout(refresh, 1000);
</script>
%if game.name:
<h1>Game:{{game.name}}</h1>
%end

<h2>Welcome {{player.name}}</h2>

<% 
    for team in ["A", "B"]:
        include("team_invite.tpl", team=team)
    end
%>
<form action="ready" method="post">
    <button>Ready</button>
</form>