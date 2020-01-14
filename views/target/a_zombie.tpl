%if len(zombies) > 0 and not (len(zombies) == 1 and is_zombie):
<option value="z" {{"selected" if defined("last_target") and last_target == "z" else ""}}>a zombie</option>\\
%end
