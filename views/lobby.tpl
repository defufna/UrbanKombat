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
<h1>{{game.name}}</h1>
%end
<h2>Welcome {{player.name}}</h2>
<div class="gp flav">

    <p>Here you can invite players to the game. The game will start once all players have clicked ready.
    %if len(game.players) == 1:
    	The button will appear, once someone joins the game.
    %end
    </p>
    <%
        for team in ["A", "B"]:
            include("team_invite.tpl", team=team)
        end
    %>
%if len(game.players) > 1:
    <form action="ready" method="post">
        <button>Ready</button>
    </form>
%end
</div>