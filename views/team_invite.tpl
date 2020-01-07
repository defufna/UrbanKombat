<p>To invite people to Team {{team}} use: <a href="{{server_name}}/{{format(game.id, "x")}}/create_char?team={{team}}">{{server_name}}/{{format(game.id, "x")}}/create_char?team={{team}}</a></p>

<p>Team {{team}}</p>

<ul>
%for player in game.team(team):
    <li>{{player.name}}\\
%if player.ready:
 ✓
%end
</li>
%end
</ul>
