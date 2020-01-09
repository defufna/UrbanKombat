<p>To invite people to Team {{team}} use: <a href="{{server_name}}/{{format(game.id, "x")}}/create_char?team={{team}}">{{server_name}}/{{format(game.id, "x")}}/create_char?team={{team}}</a></p>

<p>Team {{team}}</p>

<ul>
%for player in game.team(team):
    <li>{{player.name}}\\
    %if player.ready:
 ✓
    %end
    %if host and player is not game.host:
        <form action="kick" method="post">
            <input type="hidden" name="player_id" value="{{player.id}}">
            <button class="m">Kick</button>
        </form>
    %end
    </li>
%end
</ul>
