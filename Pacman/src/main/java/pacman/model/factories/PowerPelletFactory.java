package pacman.model.factories;

import javafx.scene.image.Image;
import pacman.ConfigurationParseException;
import pacman.model.entity.Renderable;
import pacman.model.entity.dynamic.physics.BoundingBox;
import pacman.model.entity.dynamic.physics.BoundingBoxImpl;
import pacman.model.entity.dynamic.physics.Vector2D;
import pacman.model.entity.staticentity.collectable.Pellet;
import pacman.model.entity.staticentity.collectable.PowerPellet;

/**
 * Concrete renderable factory for Pellet objects
 */
public class PowerPelletFactory implements RenderableFactory {
    private static final Image PELLET_IMAGE = new Image("maze/pellet.png");
    private static final int NUM_POINTS = 10;
    private final Renderable.Layer layer = Renderable.Layer.BACKGROUND;

    @Override
    public Renderable createRenderable(
            Vector2D position
    ) {
        try {
            position = position.add(new Vector2D(-8, -8));

            BoundingBox boundingBox = new BoundingBoxImpl(
                    position,
                    32,
                    32
            );

            Pellet pellet = new Pellet(boundingBox, layer, PELLET_IMAGE, NUM_POINTS);

            return new PowerPellet(pellet, 40);

        } catch (Exception e) {
            throw new ConfigurationParseException(
                    String.format("Invalid pellet configuration | %s", e));
        }
    }
}
