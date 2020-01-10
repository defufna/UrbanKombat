<table class="team">
    <thead>
        <tr>

            <th colspan="4">
                Team {{team}}
            </th>
        </tr>
        <tr>
            <th>Name</th>
            <th>Class</th>
            <th>Ready</th>
            %if get("host", False):
            <th>Kick</th>
            %end
        </tr>
    </thead>
    <tbody>
    %for player in game.team(team):
        <tr>
        <td>{{player.name}}</td>
        <td>{{type(player).__name__}}</td>
        <td>
        %if player.ready:
    ✓
        %end
        </td>    
        %if get("host", False):
        <td>
            %if player is not game.host:
            <form action="kick" method="post">

                <input type="hidden" name="player_id" value="{{player.id}}">
                <button class="m">Kick</button>
            </form>
            %end
        </td>
        %end
        </tr>
    %end
    </tbody>
</table>

