import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NetPositionsComponent } from './net-positions.component';

describe('NetPositionsComponent', () => {
  let component: NetPositionsComponent;
  let fixture: ComponentFixture<NetPositionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NetPositionsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NetPositionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
