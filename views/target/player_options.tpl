%for player in players:
    <option class="\\
%if player.team == team:
con5\\
%else:
con2\\
%end
    " value="{{player.id}}" {{"selected" if defined("last_target") and last_target is not None and last_target.isdigit() and int(last_target) == player.id else ""}}>{{player.name}}</option>\\
%end