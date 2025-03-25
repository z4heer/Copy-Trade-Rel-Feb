import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';
import { Holding } from '../net-positions/position.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-holdings',
  templateUrl: './holdings.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [CommonModule]
})
export class HoldingsComponent implements OnInit {
  holdings: Holding[] = [];
  error: string | null = null;

  constructor(private tradeService: TradeService,private router: Router) {}

  ngOnInit(): void {
    this.tradeService.getHoldings_all().subscribe(
      data => this.holdings = data.Holdings,
      (error) => {
        this.error = 'Failed to load holdings, please make sure RequestId is fresh session and try again';
        console.error(error);
      }
    );
  }

  call_squareoff(holding: Holding): void {
    const positionData = JSON.stringify(holding);
    //console.log('Sqaure off- order:', positionData);  
    this.router.navigate(['/square-off-position', { position: positionData }]);
  }
  
}