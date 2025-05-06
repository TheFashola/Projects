package pacman.model.entity.staticentity.collectable;

import javafx.scene.image.Image;
import pacman.model.entity.Renderable;
import pacman.model.entity.dynamic.physics.BoundingBox;
import pacman.model.entity.dynamic.physics.Vector2D;
import pacman.model.entity.staticentity.StaticEntity;

public abstract class CollectableDecorator implements PelletComponent, StaticEntity {
    protected PelletComponent decoratedCollectable;

    public CollectableDecorator(PelletComponent decoratedCollectable) {
        this.decoratedCollectable = decoratedCollectable;
    }

    @Override
    public int getPoints() {
        return decoratedCollectable.getPoints();
    }

    @Override
    public void collect() {
        decoratedCollectable.collect();
    }

    @Override
    public void reset() {
        decoratedCollectable.reset();
    }

    @Override
    public boolean isCollectable() {
        return decoratedCollectable.isCollectable();
    }

    @Override
    public boolean canPassThrough() {
        return decoratedCollectable.canPassThrough();
    }

    @Override
    public Renderable.Layer getLayer() {
        return decoratedCollectable.getLayer();
    }

    @Override
    public Image getImage() {
        return decoratedCollectable.getImage();
    }

    @Override
    public double getWidth() {
        return decoratedCollectable.getWidth();
    }

    @Override
    public double getHeight() {
        return decoratedCollectable.getHeight();
    }

    @Override
    public Vector2D getPosition() {
        return decoratedCollectable.getPosition();
    }

    @Override
    public BoundingBox getBoundingBox() {
        return decoratedCollectable.getBoundingBox();
    }
}