package pacman.model.entity.dynamic.ghost.ghostTypes;

import javafx.scene.image.Image;
import pacman.model.entity.dynamic.ghost.GhostImpl;
import pacman.model.entity.dynamic.ghost.GhostMode;
import pacman.model.entity.dynamic.physics.BoundingBox;
import pacman.model.entity.dynamic.physics.KinematicState;
import pacman.model.entity.dynamic.physics.Vector2D;

public class Clyde extends GhostImpl {
    public Clyde(Image image, BoundingBox boundingBox, KinematicState kinematicState, GhostMode ghostMode, Vector2D targetCorner) {
        super(image, boundingBox, kinematicState, ghostMode, targetCorner);
    }
}
