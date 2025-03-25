import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SquareOffPositionComponent } from './square-off-position.component';

describe('SquareOffPositionComponent', () => {
  let component: SquareOffPositionComponent;
  let fixture: ComponentFixture<SquareOffPositionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SquareOffPositionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SquareOffPositionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
