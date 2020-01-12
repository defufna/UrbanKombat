% rebase('base.tpl', title='Lobby')
<script type="text/javascript">
var data = ["{{state}}", {{lobby_version}}];

function refresh() {
    var request = new XMLHttpRequest();
    request.open('GET', 'status', true);

    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            var new_data = JSON.parse(this.response);

            if(new_data[0] != "WAITING"){
                window.location.href = "./map.cgi";
            }
            if(new_data[1] != data[1]){
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

<div class="gp">
    %if game.name:
    <h1>{{game.name}}</h1>
    %end
    <h2>Welcome {{player.name}}</h2>

    <p>Here you can invite players to the game. The game will start once all players have clicked ready.
    %if len(game.players) == 1:
    	The button will appear, once someone joins the game.
    %end
    </p>

    <p>To invite people use: <a href="{{server_name}}/{{format(game.id, "x")}}">{{server_name}}/{{format(game.id, "x")}}</a></p>

    <div>
        To switch teams click here: 
        
        <form action="switch" method="post">
            <button class="m" type="submit">Switch teams</button>
        </form>
    </div>


    <%
        for team in game.teams:
            include("team_invite.tpl", team=team)
        end
    %>
    %if len(game.players) > 1:
        <form action="ready" method="post">
            <button class="m">Ready</button>
        </form>
    %end
</div>