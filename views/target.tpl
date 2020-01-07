<select name="target">\\
%if get("include_self", False):
<option value="">self</option>\\
%end
%if zombies > 0 and not (zombies == 1 and is_zombie):
<option value="z" {{"selected" if defined("last_target") and last_target == "z" else ""}}>a zombie</option>\\
%end
%for player in humans:
    <option value="{{player.id}}" {{"selected" if defined("last_target") and last_target is not None and last_target.isdigit() and int(last_target) == player_id else ""}}>{{player.name}}</option>\\
%end
</select>