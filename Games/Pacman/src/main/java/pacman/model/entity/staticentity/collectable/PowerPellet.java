package pacman.model.entity.staticentity.collectable;

public class PowerPellet extends CollectableDecorator {
    private final int extraPoints;

    public PowerPellet(PelletComponent decoratedCollectable, int bonusPoints) {
        super(decoratedCollectable);
        this.extraPoints = bonusPoints;
    }

    @Override
    public int getPoints() {
        return super.getPoints() + extraPoints;
    }
}