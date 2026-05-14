//+------------------------------------------------------------------+
//|                                   MAW_SmartManager_V2.mq5        |
//|                        Developed for: Webzflow.com Infrastructure|
//|                                     Copyright 2026, MrAskWhy.com |
//|                                         https://www.mraskwhy.com |
//+------------------------------------------------------------------+
#property copyright "MrAskWhy (Pty) Ltd"
#property link      "https://www.mraskwhy.com"
#property version   "2.20"
#property strict

/* FAIS COMPLIANCE NOTE: 
   This software is a Trade Management Utility. It does not generate 
   buy/sell signals and does not constitute financial advice. 
*/

#include <Trade\Trade.mqh>

//--- 1. ENUMS ---
enum ENUM_STRAT_PROFILE {
    PROFILE_SCALP,
    PROFILE_SWING,
    PROFILE_BREAKOUT,
    PROFILE_DEFAULT
};

//--- 2. INPUT PARAMETERS ---
input group "=== General Settings ==="
input long   InpTargetMagic       = -1;         // Magic Number to Manage (-1 = ALL trades)
input bool   InpDetailedLogs      = true;       // Enable Detailed Audit Logging
input int    InpTimerMs           = 500;        // Management frequency (ms)

input group "=== Auto SL / TP Assignment ==="
input bool   InpAutoAssignSLTP    = true;       // Auto-assign SL/TP if missing
input int    InpAssignDelaySec    = 30;         // Wait X seconds before assigning (allow bot to set first)
input double InpDefaultSLATR      = 1.5;        // Default SL ATR Multiplier
input double InpDefaultTPATR      = 3.5;        // Default TP ATR Multiplier

input group "=== [DEFAULT] Profile Settings ==="
input double InpDefBETriggerR     = 1.2;        // Default BE Trigger (R)
input double InpDefPartial1R      = 1.5;        // Partial 1 Trigger (R)
input double InpDefPartial1Pct    = 50.0;       // Partial 1 Percent
input double InpDefTrailTriggerR  = 2.2;        // Trail Trigger (R)
input double InpDefTrailATRMult   = 3.0;        // Trail Distance (ATR)

input group "=== [SCALP] Profile Settings (Aligned) ==="
input int    InpScalpBEPips       = 20;         // Scalp BE Trigger (Pips)
input double InpScalpPartialPct   = 20.0;       // Scalp Partial Percent (20%)
input double InpScalpTrailTriggerR= 1.5;        // Scalp Trail Trigger (R)
input double InpScalpTrailATRMult = 1.2;        // Scalp Trail Distance (ATR)

input group "=== [SWING] Profile Settings ==="
input double InpSwingBETriggerR   = 1.5;        // Swing BE Trigger (R)
input double InpSwingPartial1R    = 2.0;        // Swing Partial 1 Trigger (R)
input double InpSwingPartial1Pct  = 30.0;       // Swing Partial 1 Percent
input double InpSwingPartial2R    = 3.5;        // Swing Partial 2 Trigger (R)
input double InpSwingPartial2Pct  = 30.0;       // Swing Partial 2 Percent
input double InpSwingTrailTriggerR= 2.5;        // Swing Trail Trigger (R)
input double InpSwingTrailATRMult = 2.5;        // Swing Trail Distance (ATR)

input group "=== Global Fallback Settings ==="
input int    InpGlobalBEPips      = 100;        // Global BE Fallback (Pips, -1 = OFF)
input double InpGlobalPartialPct  = 20.0;       // Global Partial % at BE (-1 = OFF)

input group "=== Weekend Safety ==="
input bool   InpWeekendClose      = false;      // Close all profit trades Friday night?
input int    InpFridayCloseHour   = 20;         // Hour to tighten/close (UTC)
input double InpWeekendTrailMult  = 0.5;        // Tighten ATR trail to this multiplier on Fri

//--- 3. GLOBAL VARIABLES ---
CTrade       m_trade;
int          m_hATR;
double       m_atrBuffer[];

// Statistics Variables
double       m_statDailyProfit  = 0;
double       m_statTotalProfit  = 0;
int          m_statTotalTrades  = 0;
int          m_statTotalWins    = 0;
double       m_statWinRate      = 0;
double       m_statDrawdown     = 0;
double       m_statProfitFactor = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit() {
    m_trade.SetExpertMagicNumber(198522); // V2.2 Unique Magic
    m_trade.SetDeviationInPoints(30);
    
    m_hATR = iATR(_Symbol, PERIOD_CURRENT, 14);
    if(m_hATR == INVALID_HANDLE) {
        Print("[CRITICAL ERROR] Failed to load ATR indicator.");
        return(INIT_FAILED);
    }
    
    ArraySetAsSeries(m_atrBuffer, true);
    EventSetMillisecondTimer(InpTimerMs);
    
    Print("==================================================");
    Print(" MAW SmartManager V2.2 Auto-Init + Strategy-Aware");
    Print(" Mode: Managing ", (InpTargetMagic == -1 ? "ALL" : "Magic " + IntegerToString(InpTargetMagic)));
    Print("==================================================");
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason) {
    IndicatorRelease(m_hATR);
    EventKillTimer();
}

//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer() { ProcessManagement(); }
void OnTick()  { ProcessManagement(); }

//+------------------------------------------------------------------+
//| Core Management Logic                                            |
//+------------------------------------------------------------------+
void UpdateStats() {
    m_statTotalProfit = AccountInfoDouble(ACCOUNT_PROFIT);
    m_statDailyProfit = 0;
    m_statTotalTrades = 0;
    m_statTotalWins   = 0;
    
    double grossProfit = 0;
    double grossLoss   = 0;
    
    if(HistorySelect(TimeCurrent() - 86400, TimeCurrent())) {
        for(int i = HistoryDealsTotal() - 1; i >= 0; i--) {
            ulong ticket = HistoryDealGetTicket(i);
            if(HistoryDealGetInteger(ticket, DEAL_MAGIC) == InpTargetMagic || InpTargetMagic == -1) {
                m_statDailyProfit += HistoryDealGetDouble(ticket, DEAL_PROFIT);
            }
        }
    }
    
    if(HistorySelect(0, TimeCurrent())) {
        for(int i = HistoryDealsTotal() - 1; i >= 0; i--) {
            ulong ticket = HistoryDealGetTicket(i);
            long type = HistoryDealGetInteger(ticket, DEAL_TYPE);
            long entry = HistoryDealGetInteger(ticket, DEAL_ENTRY);
            
            if(entry != DEAL_ENTRY_OUT) continue;
            if(InpTargetMagic != -1 && HistoryDealGetInteger(ticket, DEAL_MAGIC) != InpTargetMagic) continue;
            
            double profit = HistoryDealGetDouble(ticket, DEAL_PROFIT);
            m_statTotalTrades++;
            if(profit > 0) {
                m_statTotalWins++;
                grossProfit += profit;
            } else {
                grossLoss += MathAbs(profit);
            }
        }
    }
    
    m_statWinRate = (m_statTotalTrades > 0) ? (m_statTotalWins * 100.0 / m_statTotalTrades) : 0;
    m_statProfitFactor = (grossLoss > 0) ? (grossProfit / grossLoss) : grossProfit;
}

void DrawDashboard(string text) {
    UpdateStats();
    
    color headerClr = clrDodgerBlue;
    color textClr   = clrWhite;
    color valClr    = clrCyan;
    
    int xBase = 10;
    int yBase = 30;
    int spacing = 20;

    // Background
    string bgName = "SM_DashBG";
    if(ObjectFind(0, bgName) < 0) {
        ObjectCreate(0, bgName, OBJ_RECTANGLE_LABEL, 0, 0, 0);
        ObjectSetInteger(0, bgName, OBJPROP_XDISTANCE, xBase);
        ObjectSetInteger(0, bgName, OBJPROP_YDISTANCE, yBase);
        ObjectSetInteger(0, bgName, OBJPROP_XSIZE, 280);
        ObjectSetInteger(0, bgName, OBJPROP_YSIZE, 220);
        ObjectSetInteger(0, bgName, OBJPROP_BGCOLOR, C'20,20,20');
        ObjectSetInteger(0, bgName, OBJPROP_BORDER_TYPE, BORDER_FLAT);
        ObjectSetInteger(0, bgName, OBJPROP_CORNER, CORNER_LEFT_UPPER);
    }

    // Title
    SetLabel("SM_Title", "SMART MANAGER V2.2 - " + (InpTargetMagic == -1 ? "ALL" : "MAGIC " + (string)InpTargetMagic), xBase+10, yBase+10, 10, headerClr);
    
    // Stats
    SetLabel("SM_Profit_Label", "Total Profit:", xBase+15, yBase+40, 9, textClr);
    SetLabel("SM_Profit_Val", DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE) - 10000.0 + m_statTotalProfit, 2), xBase+150, yBase+40, 9, (m_statTotalProfit >= 0 ? clrLime : clrRed));
    
    SetLabel("SM_Daily_Label", "Daily Profit:", xBase+15, yBase+60, 9, textClr);
    SetLabel("SM_Daily_Val", DoubleToString(m_statDailyProfit, 2), xBase+150, yBase+60, 9, (m_statDailyProfit >= 0 ? clrLime : clrRed));
    
    SetLabel("SM_Trades_Label", "Total Trades:", xBase+15, yBase+85, 9, textClr);
    SetLabel("SM_Trades_Val", (string)m_statTotalTrades, xBase+150, yBase+85, 9, valClr);
    
    SetLabel("SM_WinRate_Label", "Win Rate:", xBase+15, yBase+105, 9, textClr);
    SetLabel("SM_WinRate_Val", DoubleToString(m_statWinRate, 1) + "%", xBase+150, yBase+105, 9, (m_statWinRate >= 60 ? clrLime : clrOrange));
    
    SetLabel("SM_PF_Label", "Profit Factor:", xBase+15, yBase+125, 9, textClr);
    SetLabel("SM_PF_Val", DoubleToString(m_statProfitFactor, 2), xBase+150, yBase+125, 9, (m_statProfitFactor >= 2 ? clrLime : clrWhite));

    // Daily History Table
    SetLabel("SM_Hist_Header", "LAST 7 DAYS P&L", xBase+15, yBase+155, 8, headerClr);
    
    if(HistorySelect(TimeCurrent() - 86400*7, TimeCurrent())) {
        MqlDateTime dt;
        double dayPnL[7] = {0,0,0,0,0,0,0};
        string dayNames[7];
        
        for(int d=0; d<7; d++) {
            datetime target = TimeCurrent() - 86400*d;
            TimeToStruct(target, dt);
            dayNames[d] = StringFormat("%02d/%02d", dt.day, dt.mon);
            
            for(int i = HistoryDealsTotal() - 1; i >= 0; i--) {
                ulong t = HistoryDealGetTicket(i);
                datetime dealTime = (datetime)HistoryDealGetInteger(t, DEAL_TIME);
                if(dealTime >= target - (dealTime%86400) && dealTime < target - (dealTime%86400) + 86400) {
                   if(InpTargetMagic == -1 || HistoryDealGetInteger(t, DEAL_MAGIC) == InpTargetMagic) {
                      dayPnL[d] += HistoryDealGetDouble(t, DEAL_PROFIT);
                   }
                }
            }
            
            string lblName = "SM_Day_"+(string)d;
            SetLabel(lblName+"_L", dayNames[d], xBase+15, yBase+175 + (d*15), 8, textClr);
            SetLabel(lblName+"_V", DoubleToString(dayPnL[d], 2), xBase+100, yBase+175 + (d*15), 8, (dayPnL[d] >= 0 ? clrLime : clrRed));
        }
    }

    SetLabel("SM_Last_Label", "ACTIVE POS:", xBase+15, yBase+290, 8, headerClr);
    SetLabel("SM_Last_Val", text, xBase+15, yBase+310, 8, clrYellow);
    
    // Update BG size
    ObjectSetInteger(0, "SM_DashBG", OBJPROP_YSIZE, 340);
}

void SetLabel(string name, string text, int x, int y, int size, color clr) {
    if(ObjectFind(0, name) < 0) ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);
    ObjectSetString(0, name, OBJPROP_TEXT, text);
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size);
    ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
}
void ProcessManagement() {
    if(CopyBuffer(m_hATR, 0, 0, 1, m_atrBuffer) <= 0) return;
    
    double currentATR = m_atrBuffer[0];
    double pt = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
    if(pt == 0) pt = 0.00001; 
    
    MqlDateTime dt;
    TimeGMT(dt);
    bool isFridayNight = (dt.day_of_week == 5 && dt.hour >= InpFridayCloseHour);

    DrawDashboard("Scanning for positions...");

    for(int i = PositionsTotal() - 1; i >= 0; i--) {
        ulong ticket = PositionGetTicket(i);
        if(!PositionSelectByTicket(ticket)) continue;
        if(PositionGetString(POSITION_SYMBOL) != _Symbol) continue;
        
        long magic = PositionGetInteger(POSITION_MAGIC);
        if(InpTargetMagic != -1 && magic != InpTargetMagic) continue;
        
        string comment = PositionGetString(POSITION_COMMENT);
        ENUM_STRAT_PROFILE profile = GetProfileFromComment(comment);
        
        static datetime lastLogTime = 0;
        bool shouldLog = (InpDetailedLogs && TimeCurrent() - lastLogTime >= 60); 
        if(shouldLog) lastLogTime = TimeCurrent();

        string statusText = StringFormat("Position #%I64u [%s] | Magic: %d", ticket, EnumToString(profile), magic);
        DrawDashboard(statusText);
        
        long   type   = PositionGetInteger(POSITION_TYPE);
        double open   = PositionGetDouble(POSITION_PRICE_OPEN);
        double current= PositionGetDouble(POSITION_PRICE_CURRENT);
        double sl     = PositionGetDouble(POSITION_SL);
        double tp     = PositionGetDouble(POSITION_TP);
        double vol    = PositionGetDouble(POSITION_VOLUME);
        long   posID  = PositionGetInteger(POSITION_IDENTIFIER);
        datetime time = (datetime)PositionGetInteger(POSITION_TIME);
        
        // --- 1. AUTO ASSIGN SL / TP (IF MISSING) ---
        if(InpAutoAssignSLTP && (sl == 0 || tp == 0)) {
            // Check delay
            if(TimeCurrent() - time >= InpAssignDelaySec) {
                double newSL = sl;
                double newTP = tp;
                double slATRMult = InpDefaultSLATR;
                double tpATRMult = InpDefaultTPATR;
                
                // Adjust multipliers based on profile if known
                if(profile == PROFILE_SCALP) { slATRMult = 1.0; tpATRMult = 1.5; }
                
                double dist = currentATR * slATRMult;
                if(type == POSITION_TYPE_BUY) {
                    if(newSL == 0) newSL = open - dist;
                    if(newTP == 0) newTP = open + (currentATR * tpATRMult);
                } else {
                    if(newSL == 0) newSL = open + dist;
                    if(newTP == 0) newTP = open - (currentATR * tpATRMult);
                }
                
                if(m_trade.PositionModify(ticket, NormalizeDouble(newSL, _Digits), NormalizeDouble(newTP, _Digits))) {
                    if(InpDetailedLogs) PrintFormat("[SmartManager] Auto-Initialized SL/TP on #%I64u", ticket);
                    sl = newSL; tp = newTP; // Update locals
                }
            }
        }

        // Ensure we have SL for risk calc before proceeding to BE/Trailing
        if(sl == 0) continue; 
        double baseRisk = MathAbs(open - sl);
        if(baseRisk < pt) continue; 
        
        double profitDist = (type == POSITION_TYPE_BUY) ? (current - open) : (open - current);
        double currentR = profitDist / baseRisk;

        // Resolve Profile Parameters
        double beTriggerR = InpDefBETriggerR;
        double p1TriggerR = InpDefPartial1R;
        double p1Pct      = InpDefPartial1Pct;
        double trailR     = InpDefTrailTriggerR;
        double trailATR   = InpDefTrailATRMult;
        double p2TriggerR = 999;
        double p2Pct      = 0;

        if(profile == PROFILE_SCALP) {
            beTriggerR = 0; // Handled by pips logic below
            p1TriggerR = 0; // Handled by pips logic below
            p1Pct      = InpScalpPartialPct;
            trailR     = InpScalpTrailTriggerR;
            trailATR   = InpScalpTrailATRMult;
        } else if(profile == PROFILE_SWING) {
            beTriggerR = InpSwingBETriggerR;
            p1TriggerR = InpSwingPartial1R;
            p1Pct      = InpSwingPartial1Pct;
            p2TriggerR = InpSwingPartial2R;
            p2Pct      = InpSwingPartial2Pct;
            trailR     = InpSwingTrailTriggerR;
            trailATR   = InpSwingTrailATRMult;
        }

        if(isFridayNight) { trailATR *= InpWeekendTrailMult; trailR = 0.5; }

        // 2. BREAK EVEN
        bool triggerBE = false;
        double globalBEThresh = (InpGlobalBEPips > 0) ? (InpGlobalBEPips * 10 * pt) : 999999;
        
        if(profile == PROFILE_SCALP) {
            triggerBE = (profitDist >= InpScalpBEPips * 10 * pt); 
        } else {
            triggerBE = (currentR >= beTriggerR);
        }

        // Fallback: Whichever comes first
        if(!triggerBE && InpGlobalBEPips > 0 && profitDist >= globalBEThresh) {
            triggerBE = true;
            if(shouldLog) PrintFormat("[SmartManager] #%I64u Triggering BE via Global Fallback (%d pips)", ticket, InpGlobalBEPips);
        }

        if(shouldLog && !triggerBE) {
            double targetPips = (profile == PROFILE_SCALP) ? InpScalpBEPips : (beTriggerR * baseRisk / (10*pt));
            if(InpGlobalBEPips > 0 && InpGlobalBEPips < targetPips) targetPips = InpGlobalBEPips;
            PrintFormat("[SmartManager] #%I64u [%s] Profit: %.1f pips | BE Target: %.1f pips", 
                        ticket, EnumToString(profile), profitDist/(10*pt), targetPips);
        }

        if(triggerBE) {
            double newBE = (type == POSITION_TYPE_BUY) ? (open + 10 * pt) : (open - 10 * pt);
            if((type == POSITION_TYPE_BUY && sl < newBE) || (type == POSITION_TYPE_SELL && (sl > newBE || sl == 0))) {
                if(m_trade.PositionModify(ticket, NormalizeDouble(newBE, _Digits), tp)) {
                    PrintFormat("[SmartManager] BE Secured on #%I64u at %.5f (Profile: %s)", ticket, newBE, EnumToString(profile));
                    sl = newBE;
                }
            }
        }

        // 3. PARTIALS
        int partialCount = GetPartialCount(posID);
        if(partialCount == 0) {
           bool triggerP1 = false;
           double pPct = p1Pct;
           if(profile == PROFILE_SCALP) {
               triggerP1 = (profitDist >= InpScalpBEPips * 10 * pt); // Take partial at BE trigger
               pPct = InpScalpPartialPct;
           } else {
               triggerP1 = (currentR >= p1TriggerR);
           }
           
           // Global Partial Fallback
           if(!triggerP1 && InpGlobalBEPips > 0 && profitDist >= globalBEThresh && InpGlobalPartialPct > 0) {
               triggerP1 = true;
               pPct = InpGlobalPartialPct;
           }

           if(triggerP1) {
               if(TakePartial(ticket, vol, pPct, profile, 1)) vol = PositionGetDouble(POSITION_VOLUME);
           }
        }
        if(partialCount == 1 && currentR >= p2TriggerR) TakePartial(ticket, vol, p2Pct, profile, 2);

        // 4. SMART TRAILING
        if(currentR >= trailR) {
            double trailDist = currentATR * trailATR;
            double targetSL = (type == POSITION_TYPE_BUY) ? (current - trailDist) : (current + trailDist);
            bool shouldMove = (type == POSITION_TYPE_BUY) ? (targetSL > sl + 20*pt) : (targetSL < sl - 20*pt || sl == 0);
            if(shouldMove) m_trade.PositionModify(ticket, NormalizeDouble(targetSL, _Digits), tp);
        }
    }
}

ENUM_STRAT_PROFILE GetProfileFromComment(string comment) {
    string low = comment; StringToLower(low);
    // Scalp Profiles
    if(StringFind(low, "scalp") >= 0 || StringFind(low, "mql") >= 0 || StringFind(low, "orb") >= 0) return PROFILE_SCALP;
    // Swing & Trend Profiles
    if(StringFind(low, "swing") >= 0 || StringFind(low, "trend") >= 0 || StringFind(low, "fractal") >= 0 || 
       StringFind(low, "pull") >= 0 || StringFind(low, "div") >= 0 || StringFind(low, "confluence") >= 0 ||
       StringFind(low, "rsi") >= 0 || StringFind(low, "macd") >= 0 || StringFind(low, "ma") >= 0) return PROFILE_SWING;
    // Breakout & Momentum Profiles
    if(StringFind(low, "breakout") >= 0 || StringFind(low, "squeeze") >= 0 || StringFind(low, "donchian") >= 0 || 
       StringFind(low, "momentum") >= 0 || StringFind(low, "turtle") >= 0) return PROFILE_BREAKOUT;
    
    return PROFILE_DEFAULT;
}

bool TakePartial(ulong ticket, double currentVol, double pct, ENUM_STRAT_PROFILE profile, int stage) {
    double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
    double closeVol = MathFloor((currentVol * (pct / 100.0)) / stepLot) * stepLot;
    if(closeVol >= minLot && closeVol < currentVol) {
        if(m_trade.PositionClosePartial(ticket, closeVol)) {
            if(InpDetailedLogs) PrintFormat("[%s] Partial %d (%.2f lots) closed on #%I64u", EnumToString(profile), stage, closeVol, ticket);
            return true;
        }
    }
    return false;
}

int GetPartialCount(long positionID) {
    int count = 0; if(HistorySelectByPosition(positionID)) {
        int totalDeals = HistoryDealsTotal();
        for(int i = 0; i < totalDeals; i++) {
            ulong ticket = HistoryDealGetTicket(i);
            if(HistoryDealGetInteger(ticket, DEAL_ENTRY) == DEAL_ENTRY_OUT) count++;
        }
    }
    return count;
}

