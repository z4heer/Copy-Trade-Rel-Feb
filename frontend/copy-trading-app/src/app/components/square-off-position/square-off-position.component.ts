import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-square-off-position',
  templateUrl: './square-off-position.component.html',
  styleUrls: ['./square-off-position.component.css'],
  imports: [ReactiveFormsModule, CommonModule] // Add ReactiveFormsModule to imports  
})
export class SquareOffPositionComponent implements OnInit {
  squareOffForm: FormGroup;
  error: string | null = null;

  constructor(private fb: FormBuilder) {
    this.squareOffForm = this.fb.group({
      sqrLst: this.fb.array([])
    });
  }

  ngOnInit(): void {
    this.addSquareOff();
  }

  get sqrLst(): FormArray {
    return this.squareOffForm.get('sqrLst') as FormArray;
  }

  addSquareOff(): void {
    this.sqrLst.push(this.fb.group({
      TradingSymbol: ['', Validators.required],
      Exchange: ['', Validators.required],
      Action: ['', Validators.required],
      Duration: ['', Validators.required],
      OrderType: ['', Validators.required],
      Quantity: ['', Validators.required],
      ProductCode: ['', Validators.required],
      StreamingSymbol: ['', Validators.required],
      Price: ['', Validators.required],
      DisclosedQuantity: ['', Validators.required],
      GTDDate: ['NA', Validators.required],
      Remark: ['Closing positions', Validators.required],
      TriggerPrice: ['', Validators.required]
    }));
  }

  squareOff(): void {
    if (this.squareOffForm.valid) {
      // Implement the logic to square off the position here
      console.log('Square off form submitted:', this.squareOffForm.value);
    } else {
      this.error = 'Please fill out all required fields.';
    }
  }
}