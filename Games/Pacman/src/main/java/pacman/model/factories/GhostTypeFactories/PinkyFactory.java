package pacman.model.factories.GhostTypeFactories;

import javafx.scene.image.Image;
import pacman.model.entity.Renderable;
import pacman.model.entity.dynamic.ghost.GhostImpl;
import pacman.model.entity.dynamic.ghost.GhostMode;
import pacman.model.entity.dynamic.physics.BoundingBox;
import pacman.model.entity.dynamic.physics.KinematicState;
import pacman.model.entity.dynamic.physics.Vector2D;
import pacman.model.factories.GhostFactory;
import pacman.model.entity.dynamic.ghost.ghostTypes.*;


public class PinkyFactory extends GhostFactory {

    private static final Image PINKY_IMAGE = new Image("maze/ghosts/pinky.png");

    @Override
    protected Image getImage() {
        return PINKY_IMAGE;
    }

    @Override
    public Renderable createRenderable(Vector2D position) {
        return super.createRenderable(position);
    }

    @Override
    public GhostImpl getGhost(Image image, BoundingBox boundingBox, KinematicState kinematicState, GhostMode ghostMode, Vector2D targetCorner) {
        return new Pinky(image, boundingBox, kinematicState, ghostMode, targetCorner);
    }
}
