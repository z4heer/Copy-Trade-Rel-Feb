import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { TradeService } from '../../services/trade.service';

@Component({
  selector: 'app-square-off-position',
  templateUrl: './square-off-position.component.html',
  styleUrls: ['./square-off-position.component.css'],
  imports: [ReactiveFormsModule, CommonModule]
})
export class SquareOffPositionComponent implements OnInit {
  squareOffForm: FormGroup;
  error: string | null = null;

  constructor(private fb: FormBuilder, private route: ActivatedRoute, private router: Router,
    private tradeService: TradeService
  ) {
    this.squareOffForm = this.fb.group({
      sqrLst: this.fb.array([])
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const positionData = params['position'];
      console.log('Square off:', positionData);  
      if (positionData) {
        const position = JSON.parse(positionData);
        this.addSquareOff(position);
      } else {
        console.error('No position data found in route parameters');
      }
    });
  }

  get sqrLst(): FormArray {
    return this.squareOffForm.get('sqrLst') as FormArray;
  }

  addSquareOff(position: any): void {
    const price = position.BuyPrice !== 0 ? position.BuyPrice : position.Ltp;
    this.sqrLst.push(this.fb.group({
      userid: [position.userid, Validators.required],
      symbol: [position.Symbol, Validators.required],
      TradingSymbol: [position.TradingSymbol, Validators.required],
      Exchange: [position.Exchange, Validators.required],
      Action: [position.squareOffAction, Validators.required],
      Duration: ['DAY', Validators.required],
      OrderType: ['LIMIT', Validators.required],
      Quantity: [position.BuyQuantity, Validators.required],
      ProductCode: [position.ProductCode, Validators.required],
      StreamingSymbol: [position.StreamingSymbol, Validators.required],
      Price: [price, Validators.required],
      DisclosedQuantity: [0, Validators.required],
      GTDDate: ['NA', Validators.required],
      Remark: ['Closing positions', Validators.required],
      TriggerPrice: [position.BuyPrice, Validators.required]
    }));
  }

  squareOff(): void {
    if (this.squareOffForm.invalid) {
      this.error = 'Square off Position form is invalid';
      return;
    }
    const formValue = this.squareOffForm.value;
    const payload = {
      userid: formValue.sqrLst[0].userid,
      sqrLst: formValue.sqrLst.map((sqr: any) => ({
        TradingSymbol: sqr.TradingSymbol,
        Exchange: sqr.Exchange,
        Action: sqr.Action,
        Duration: sqr.Duration,
        OrderType: sqr.OrderType,
        Quantity: Number(sqr.Quantity),
        ProductCode: sqr.ProductCode,
        StreamingSymbol: sqr.StreamingSymbol,
        Price: sqr.Price,
        DisclosedQuantity: sqr.DisclosedQuantity,
        GTDDate: sqr.GTDDate,
        Remark: sqr.Remark,
        TriggerPrice: sqr.TriggerPrice
      }))
    };

    console.log('Square off payload:', payload);
  
    this.tradeService.squareOff(payload).subscribe(
      () => {
        this.error = null;
        alert('Square off completed successfully');
        this.router.navigate(['/orders']);
      },
      (error) => {
        this.error = 'Failed to Square off position';
        console.error(error);
      }
    );  
 }
}