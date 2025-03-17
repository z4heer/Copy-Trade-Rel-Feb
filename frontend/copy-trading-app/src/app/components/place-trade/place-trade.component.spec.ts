import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaceTradeComponent } from './place-trade.component';

describe('PlaceTradeComponent', () => {
  let component: PlaceTradeComponent;
  let fixture: ComponentFixture<PlaceTradeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlaceTradeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlaceTradeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
