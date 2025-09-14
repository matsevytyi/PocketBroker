"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, Brain, Mic } from "lucide-react";

export function Hero() {
  return (
    <div className="flex flex-col lg:flex-row items-center justify-between gap-8 lg:gap-12 min-h-[80vh] py-12 lg:py-20">
      {/* Left Content */}
      <div className="flex-1 space-y-6 lg:space-y-8">
        <div className="space-y-3 lg:space-y-4">
          <h1 className="text-3xl sm:text-4xl lg:text-6xl font-bold tracking-tight leading-tight">
            Your AI{" "}
            <span className="text-personality">
              Voice Broker
            </span>
          </h1>
          <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl leading-relaxed">
            Stop making stupid crypto trades. Let our AI voice agent research and invest for you like a seasoned Wall Street broker.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row flex-wrap gap-3 sm:gap-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Shield className="h-4 w-4 text-personality flex-shrink-0" />
            <span>Research Before Every Trade</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Brain className="h-4 w-4 text-personality flex-shrink-0" />
            <span>AI-Powered Analysis</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Mic className="h-4 w-4 text-personality flex-shrink-0" />
            <span>Order with natural Voice Commands</span>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
          <Button size="lg" className="bg-personality hover:bg-personality/90 text-black w-full sm:w-auto">
            Start Trading Smart
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
          <Button variant="outline" size="lg" className="w-full sm:w-auto">
            Watch Demo
          </Button>
        </div>

        <p className="text-sm text-muted-foreground">
          &ldquo;Like having Jordan Belfort in your pocket, but smarter and less likely to get you arrested.&rdquo;
        </p>
      </div>

      {/* Right Phone Preview */}
      <div className="flex-1 flex justify-center mt-8 lg:mt-0">
        <div className="relative">
          {/* Phone Frame */}
          <div className="w-48 sm:w-56 lg:w-64 h-[380px] sm:h-[450px] lg:h-[500px] bg-gray-900 rounded-[2rem] sm:rounded-[2.5rem] p-1.5 sm:p-2 shadow-2xl">
            <div className="w-full h-full bg-black rounded-[1.5rem] sm:rounded-[2rem] overflow-hidden relative">
              {/* Screen Content */}
              <div className="absolute inset-0 bg-personality/10">
                <div className="p-4 sm:p-6 h-full flex flex-col justify-between">
                  {/* Header */}
                  <div className="text-center">
                    <div className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 bg-personality rounded-full mx-auto mb-2 sm:mb-3 flex items-center justify-center">
                      <Mic className="h-4 w-4 sm:h-5 sm:w-5 lg:h-6 lg:w-6 text-black" />
                    </div>
                    <h3 className="text-white font-semibold text-sm sm:text-base lg:text-lg">PocketBroker</h3>
                    <p className="text-gray-400 text-xs sm:text-sm">AI Voice Agent</p>
                  </div>

                  {/* Middle Content */}
                  <div className="space-y-2 sm:space-y-3 lg:space-y-4">
                    <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 sm:p-4">
                      <p className="text-white text-xs sm:text-sm">
                        &ldquo;Hey PocketBroker, should I buy Bitcoin?&rdquo;
                      </p>
                    </div>
                    <div className="bg-personality/20 backdrop-blur-sm rounded-lg p-3 sm:p-4">
                      <p className="text-white text-xs sm:text-sm">
                        &ldquo;Based on market analysis, Bitcoin shows strong support at $42K. Consider a small position...&rdquo;
                      </p>
                    </div>
                  </div>

                  {/* Bottom */}
                  <div className="text-center">
                    <div className="w-6 h-6 sm:w-7 sm:h-7 lg:w-8 lg:h-8 bg-personality rounded-full mx-auto"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Floating Elements */}
          <div className="absolute -top-2 sm:-top-3 lg:-top-4 -right-2 sm:-right-3 lg:-right-4 w-6 h-6 sm:w-7 sm:h-7 lg:w-8 lg:h-8 bg-personality rounded-full animate-pulse"></div>
          <div className="absolute -bottom-2 sm:-bottom-3 lg:-bottom-4 -left-2 sm:-left-3 lg:-left-4 w-4 h-4 sm:w-5 sm:h-5 lg:w-6 lg:h-6 bg-personality rounded-full animate-pulse delay-1000"></div>
        </div>
      </div>
    </div>
  );
}
