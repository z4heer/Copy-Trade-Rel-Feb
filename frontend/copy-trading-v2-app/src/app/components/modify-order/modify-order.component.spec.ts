import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifyOrderComponent } from './modify-order.component';

describe('ModifyOrderComponent', () => {
  let component: ModifyOrderComponent;
  let fixture: ComponentFixture<ModifyOrderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModifyOrderComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModifyOrderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
