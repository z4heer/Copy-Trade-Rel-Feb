import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { HoldingResponse, NetPositionResponse } from '../components/net-positions/position.model';

@Injectable({
  providedIn: 'root'
})
export class TradeService {
  private baseUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/users`);
  }

  placeTrade(tradeDetails: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/place_trade`, tradeDetails);
  }

  getOrders(): Observable<any[]> {
    return this.http.post<any[]>(`${this.baseUrl}/orders`, { userid: '45937331' });
  }

  getTrades(): Observable<any[]> {
    return this.http.post<any[]>(`${this.baseUrl}/trades`, { userid: '45937331' });
  }

  getNetPositions(): Observable<NetPositionResponse> {
    return this.http.post<NetPositionResponse>(`${this.baseUrl}/net_position_all_users`, { userid: '45937331' });
  }

  getHoldings(): Observable<any[]> {
    return this.http.post<any[]>(`${this.baseUrl}/holdings`, { userid: '45937331' });
  }

  getHoldings_all(): Observable<HoldingResponse> {
    return this.http.post<HoldingResponse>(`${this.baseUrl}/holdings_all_users`, { });
  }

  getIsin(symbol: string): Observable<string> {
    return this.http.get<string>(`${this.baseUrl}/isin?symbol=${symbol}`);
  }

  modifyOrder(orderDetails: any): Observable<any> {
    return this.http.put<any>(`${this.baseUrl}/modify_trade/${orderDetails.userid}`, orderDetails);
  }

  cancelOrder(orderDetails: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/cancel_trade`, orderDetails);
  }

  squareOff(positionDetails: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/square-off-position`, positionDetails);
  }

}