package pacman.model.entity.staticentity.collectable;

public interface PelletComponent extends Collectable {
    int getPoints();
    void collect();
    void reset();
    boolean isCollectable();
    boolean canPassThrough();
}
